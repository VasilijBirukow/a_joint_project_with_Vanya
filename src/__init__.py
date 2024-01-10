from threading import Thread

from flask import Flask, request, render_template, jsonify, Blueprint

from changelog import get_changelog_data, get_changes_for_version, get_filtered_versions
from tools import get_config_data, run_update_script, run_restart_script, set_server_files
from wikipediaParser import parse_article

app = Flask(__name__, template_folder='../templates', static_folder='../static')

blueprint = Blueprint('study', __name__, url_prefix='/study')


@blueprint.route('/', methods=['GET'])
def main():
    return render_template('panel.html')


@blueprint.route('/article', methods=['POST'])
def get_article():
    url = request.form.get('url')
    if url:
        text = parse_article(url)
        return render_template('panel.html', article=text)


@blueprint.route('/update', methods=['POST'])
def github_webhook():
    data = request.json

    if 'ref' in data and data['ref'] == 'refs/heads/master':
        try:
            update_thread = Thread(target=run_update_script(prefix_path))
            update_thread.start()
            update_thread.join()

            config_info = get_config_data(f'{prefix_path}/config.yaml')

            current_version = config_info['current_version']
            status = f'Update success: current version is {current_version}'

            restart_thread = Thread(target=run_restart_script(prefix_path))
            restart_thread.start()

        except Exception:
            status = 'Error'
    else:
        status = 'Invalid Ref'

    return jsonify({'message': 'Webhook received', 'status': status})


@blueprint.route('/changelog', methods=['GET'])
def get_changelog():
    changelog_type = request.args.get('changelogType')
    if not changelog_type:
        return render_template('changelog.html')

    is_minor = changelog_type == 'minor'
    is_patch = changelog_type == 'patch'

    changelog_data = get_changelog_data(prefix_path)
    filtered_versions = get_filtered_versions(changelog_data, is_minor, is_patch)
    filtered_changes = {}
    for version in filtered_versions:
        filtered_changes[version] = get_changes_for_version(changelog_data, version)

    return jsonify(filtered_changes)


app.register_blueprint(blueprint)

if __name__ == '__main__':
    config_data = get_config_data()
    prefix_path = config_data['prefix_path']
    port = config_data['port']

    if config_data['current_version'] == '0.0.0':
        set_thread = Thread(target=set_server_files(prefix_path))
        set_thread.start()
        set_thread.join()

        restart_thread = Thread(target=run_restart_script(prefix_path))
        restart_thread.start()
        exit(0)

    app.run(host='0.0.0.0', port=port)
