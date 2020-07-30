import argparse
import os

REPORT_DIR = "reports"


def _run_coverage_(run_type):
    out_directory = os.path.join(REPORT_DIR, "coverage")
    if run_type == "xml":
        out_directory = os.path.join(out_directory, "coverage.xml")
        os.system('coverage run --source app -m unittest discover -s tests && coverage xml -o ' + out_directory)
    elif run_type == "html":
        out_directory = os.path.join(out_directory, "html")
        os.system('coverage run --source app -m unittest discover -s tests && coverage html -d ' + out_directory)

    print("Coverage output directory: " + out_directory)


def __setup__():
    os.system('pip3 install -r requirements.txt')
    os.system('pip3 install -r requirements.test.txt')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('script_type', help="server | test | coverage | coverage/xml")
    args = parser.parse_args()

    script_type = args.script_type

    if script_type == 'setup':
        __setup__()

    elif script_type == 'server':
        from app.main import app
        import uvicorn
        from app.util.config_manager import ConfigManager

        server_config = ConfigManager.get_config_section(section="server")
        uvicorn.run(app, host=server_config["host"], port=int(server_config["port"]))

    elif script_type == 'coverage' or script_type == 'coverage/html':
        _run_coverage_("html")

    elif script_type == 'coverage/xml':
        _run_coverage_("xml")

    elif script_type == 'test':
        os.system('python -m unittest discover -s tests')
    else:
        print("invalid script name - server | test | coverage/html | coverage/xml")
