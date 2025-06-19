import os
import argparse
import glob
import json
from utils import *

# comment: test
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--spn-auth", action="store_true", default=True)
parser.add_argument("--environment", default="development")
parser.add_argument("--config-file", default="./config/config.json")
parser.add_argument("--capacity", default=None, help="Capacity name")
parser.add_argument("--src-name", default=None, help="Nombre del proyecto")
parser.add_argument("--workspace", default=None, help="Workspace name")
parser.add_argument("--admin-upns", default=None, help="Admin UPNs, separados por comas")

args = parser.parse_args()

current_file = __file__
current_folder = os.path.dirname(current_file)
src_folder = os.path.join(current_folder, "..", "src")

# Deployment parameters:
spn_auth = args.spn_auth
environment = args.environment
capacity_name = args.capacity
src_name = args.src_name
workspace_name = args.workspace
admin_upns = args.admin_upns.split(",") if args.admin_upns else []

config = read_pbip_jsonfile(args.config_file)
configEnv = config[args.environment]

# Use command-line arguments if provided, otherwise fallback to config values
capacity_name = capacity_name or configEnv.get("capacity")
src_name = src_name or configEnv.get("srcName")
workspace_name = workspace_name or configEnv["workspace"]
admin_upns = admin_upns or configEnv.get("adminUPNs", "").split(",")
semanticmodel_parameters = configEnv.get("semanticModelsParameters", None)
server = semanticmodel_parameters.get("SqlServerInstance", None)
database = semanticmodel_parameters.get("SqlServerDatabase", None)

# Authentication
if spn_auth:
    fab_authenticate_spn()

# Ensure workspace exists
workspace_id = create_workspace(workspace_name=workspace_name, capacity_name=capacity_name, upns=admin_upns)

# Deploy semantic model
semanticmodel_path = os.path.join("src", f"{src_name}.SemanticModel")
if os.path.exists(semanticmodel_path):
    semanticmodel_id = deploy_item(
        semanticmodel_path,
        workspace_name=workspace_name,
        find_and_replace={
            (
                r"expressions.tmdl",
                r'(expression\s+SqlServerInstance\s*=\s*)".*?"',
            ): rf'\1"{server}"',
            (
                r"expressions.tmdl",
                r'(expression\s+SqlServerDatabase\s*=\s*)".*?"',
            ): rf'\1"{database}"',
        },
    )
else:
    semanticmodel_id = None

# Deploy report
report_path = os.path.join("src", f"{src_name}.Report")
if os.path.exists(report_path):
    deploy_item(
        report_path,
        workspace_name=workspace_name,
        find_and_replace={
            ("definition.pbir", r"\{[\s\S]*\}"): json.dumps(
                {
                    "version": "4.0",
                    "datasetReference": {
                        "byConnection": {
                            "connectionString": None,
                            "pbiServiceModelId": None,
                            "pbiModelVirtualServerName": "sobe_wowvirtualserver",
                            "pbiModelDatabaseName": semanticmodel_id,
                            "name": "EntityDataSource",
                            "connectionType": "pbiServiceXmlaStyleLive",
                        }
                    },
                }
            )
        },
    )

run_fab_command("auth logout")