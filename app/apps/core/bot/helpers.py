from aiogram.types import Message
from app.apps.core.bot.services.responder import Responder
from app.apps.core.bot.services.messager import Messager
from aiogram.utils.formatting import Text
import random
import requests
import datetime
import xml.etree.ElementTree as ET


def messager(method: str = '', *args) -> Messager | Text:
    if method and hasattr(Messager, method) and callable(func := getattr(Messager, method)):
        return func(*args)
    return Messager


async def answer(m: Message, text, *args):
    return await Responder(m).answer(text, *args)


def get_chats_sending_id():
    return random.randint(3, 5)


def get_debtor_info(iin):
    api_key = '124ba359ba6745bf9d2c149a8dd0e273'
    payload = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://soap.opendata.egov.nitec.kz/">
        <soapenv:Header/>
        <soapenv:Body>
            <soap:request>
            <request>
                <requestInfo>
                    <messageId>7355bcb8-fcbe-4f14-83b7-392a7a79945d</messageId>
                    <messageDate>{datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+05:00")}</messageDate>
                    <indexName>aisoip</indexName>
                    <apiKey>{api_key}</apiKey>
                </requestInfo>
                <requestData>
                    <data xmlns:ns2pep="http://bip.bee.kz/SyncChannel/v10/Types/Request" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="ns2pep:RequestMessage">
                        <iinOrBin>{iin}</iinOrBin>
                    </data>
                </requestData>
            </request>
            </soap:request>
        </soapenv:Body>
        </soapenv:Envelope>"""

    url = 'https://data.egov.kz/egov-opendata-ws/ODWebServiceImpl'

    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    def parseDept(row):
        obj = {}
        if (row.find('ilOrganRu') != None):
            obj['ilOrganRu'] = row.find('ilOrganRu').text

        if (row.find('ilDate') != None):
            obj['ilDate'] = row.find('ilDate').text

        if (row.find('debtorName') != None):
            obj['firstname'] = row.find('debtorName').text

        if (row.find('debtorSecondname') != None):
            obj['lastname'] = row.find('debtorSecondname').text

        if (row.find('recovererTitle') != None):
            obj['recoverer'] = row.find('recovererTitle').text
        else:
            obj['recoverer'] = row.find('recovererTypeRu').text

        if (row.find('recoveryAmount') != None):
            obj['recovery_amount'] = row.find('recoveryAmount').text

        if (row.find('disaNameRu') != None):
            obj['bailiffs'] = row.find('disaNameRu').text + ' ' + row.find('officerSurname').text + \
                ' ' + row.find('officerName').text + ' ' + \
                row.find('officerSecondname').text

        # if (row.find('bailiffs') != None):
        #     obj['bailiff_contact'] = row.find('disaDate').text

        return obj

    def parseResponse(response):
        responseXml = ET.fromstring(response.text)
        namespaces = {
            'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
            'ns1': 'http://soap.opendata.egov.nitec.kz/',
        }

        body_resp = responseXml.find(
            './soap:Body',
            namespaces
        )

        body = body_resp.find('./ns1:requestResponse',
                              namespaces).find('response')
        response_title = body.find('responseInfo').find(
            'status').find('message').text

        if (response_title == 'Данные не найдены'):
            return None

        if (response_title == 'Сервис отработал штатно'):
            data = []
            rows = body.find('responseData').find('data').findall('rows')
            for row in rows:
                data.append(parseDept(row))

            return data

    return parseResponse(response)
