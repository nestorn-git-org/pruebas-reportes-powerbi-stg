import os
import shutil
import subprocess
import re
import json


current_folder = os.path.dirname(__file__)
debug = False

def fab_authenticate_spn():
    client_id = os.getenv("FABRIC_CLIENT_ID")
    client_secret = os.getenv("FABRIC_CLIENT_SECRET")
    tenant_id = os.getenv("FABRIC_TENANT_ID")

    print("Authenticating with SPN")
    
    if not all([client_id, client_secret, tenant_id]):
        raise Exception("FABRIC_CLIENT_ID, FABRIC_CLIENT_SECRET and FABRIC_TENANT_ID are required")

    run_fab_command("config set fab_encryption_fallback_enabled true")

    run_fab_command(
        f"auth login -u {client_id} -p {client_secret} --tenant {tenant_id}",
        include_secrets=True
    )
    
    print("SPN authenticated successfully!")  


def run_fab_command(
    command, 
        capture_output: bool = False, 
        include_secrets: bool = False,
        silently_continue: bool = False
    ):
    
    result = subprocess.run(
        f"fab {command}",
        capture_output=capture_output,
        text=True,
        shell=True
    )


    if not (silently_continue) and (result.returncode > 0 or result.stderr):
        raise Exception(
            f"Error running fab command. exit_code: '{result.returncode}'; stderr: '{result.stderr}'"
        )

    if capture_output:

        output = result.stdout.strip().split("\n")[-1]

        return output


def create_workspace(workspace_name, capacity_name: str = "none", upns: list = None):

    print(f"::group::Creating workspace: {workspace_name}")

    command = f"create /{workspace_name}.Workspace"

    if capacity_name:
        command += f" -P capacityName={capacity_name}"

    run_fab_command(command, silently_continue=True)

    if upns is not None:

        upns = [x for x in upns if x.strip()]

        if len(upns) > 0:
            print(f"Adding UPNs")

            for upn in upns:
                run_fab_command(f"acl set -f /{workspace_name}.Workspace -I {upn} -R admin")

    print(f"::endgroup::")


def copy_to_staging(path):

    # ensure staging folder exists

    path_staging = os.path.join(current_folder, "_stg", os.path.basename(path))

    if os.path.exists(path_staging):
        shutil.rmtree(path_staging)

    os.makedirs(path_staging)

    # copy files to staging folder

    shutil.copytree(path, path_staging, dirs_exist_ok=True)

    return path_staging


def read_pbip_jsonfile(path):

    if not os.path.exists(path):
        raise Exception(f"Cannot find file: '{path}'")

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def deploy_item(
    src_path,
    workspace_name,
    item_type: str = None,
    item_name: str = None,
    find_and_replace: dict = None,
    what_if: bool = False,
    func_after_staging=None,
):

    staging_path = copy_to_staging(src_path)

    # Call function that provides flexibility to change something in the staging files

    if func_after_staging:
        func_after_staging(staging_path)

    if os.path.exists(os.path.join(staging_path, ".platform")):

        with open(os.path.join(staging_path, ".platform"), "r", encoding="utf-8") as file:
            platform_data = json.load(file)

        if item_name is None:
            item_name = platform_data["metadata"]["displayName"]

        if item_type is None:
            item_type = platform_data["metadata"]["type"]

    # Loop through all files and apply the find & replace with regular expressions

    if find_and_replace:

        for root, _, files in os.walk(staging_path):
            for file in files:

                file_path = os.path.join(root, file)

                with open(file_path, "r", encoding="utf-8", errors='replace') as file:
                    text = file.read()

                # Loop parameters and execute the find & replace in the ones that match the file path

                for key, replace_value in find_and_replace.items():

                    find_and_replace_file_filter = key[0]

                    find_and_replace_file_find = key[1]

                    if re.search(find_and_replace_file_filter, file_path):
                        text, count_subs = re.subn(
                            find_and_replace_file_find, replace_value, text
                        )

                        if count_subs > 0:

                            print(
                                f"Find & replace in file '{file_path}' with regex '{find_and_replace_file_find}'"
                            )

                            with open(file_path, "w", encoding="utf-8") as file:
                                file.write(text)
    if not what_if:
        run_fab_command(
            f"import -f /{workspace_name}.workspace/{item_name}.{item_type} -i {staging_path}"
        )

        # Return id after deployment

        item_id = run_fab_command(
            f"get /{workspace_name}.workspace/{item_name}.{item_type} -q id",
            capture_output=True,
        )

        return item_id

    print(f"::endgroup::")