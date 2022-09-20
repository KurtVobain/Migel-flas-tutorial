import json
import requests
from flask_babel import _
from app import app


def get_iam_token():
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = str({"yandexPassportOauthToken": app.config["YANDEX_OAUTH"]})

    r = requests.post(
        "https://iam.api.cloud.yandex.net/iam/v1/tokens", headers=headers, data=data
    )

    if r.status_code != 200:
        return "Error"

    return r.json().get("iamToken")


def translate(text, source_language, dest_language):
    if ("FOLDER_ID" not in app.config or not app.config["FOLDER_ID"]) or (
        "YANDEX_OAUTH" not in app.config or not app.config["YANDEX_OAUTH"]
    ):
        return _("Error: the translation service is not configured.")

    iam_token = get_iam_token()

    if iam_token == "Error":
        return _("Error: the translation service failed.")

    body = {
        "targetLanguageCode": dest_language,
        "texts": text,
        "folderId": app.config["FOLDER_ID"],
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(iam_token),
    }

    r = requests.post(
        "https://translate.api.cloud.yandex.net/translate/v2/translate",
        json=body,
        headers=headers,
    )

    if r.status_code != 200:
        return _("Error: the translation service failed.")

    return r.json().get('translations')[0].get('text')
