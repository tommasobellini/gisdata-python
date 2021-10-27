import asyncio
import logging
from datetime import datetime

import aiocron
from models import Utenti, Operazioni

logging.basicConfig(level=logging.INFO)


async def create_report(utente):
    """
    Funzione asyncrona che genera il report effettivo del singolo utente
    :param utente:
    :return:
    """
    nome_file = "./reports/{}.txt".format(utente.id)
    f = open(nome_file, "w+")
    f.write(utente.nome)
    logging.info("Processando report per {}".format(utente.nome))
    operazioni = Operazioni.filter(utente_id=utente.id).order_by(Operazioni.giorno)
    logging.info("Trovate {} operazioni di {}".format(len(operazioni), utente.nome))
    if len(operazioni) > 0:
        f.write('\n\n')
    total_operations = 0
    for operazione in operazioni:
        total_operations += operazione.ammontare
        f.write("{} ** € {}".format(operazione.giorno.strftime('%d/%m/%Y'), operazione.ammontare) + '\n')
        logging.info("{} ** € {}".format(operazione.giorno.strftime('%d/%m/%Y'), operazione.ammontare))
    try:
        utente.saldo = utente.primo_deposito + total_operations
        utente.save()
        f.close()
        logging.info("Report {} per {} completato correttamente.".format(nome_file, utente.nome))
    except Exception as e:
        logging.error("Errore durante l'aggiornamento del saldo. Dettaglio errore: {}".format(e.__str__()))


# crontab del pacchetto aiocron, schedulato ogni mezzanotte
# (per testare si può sostituire lo 0 con un *, in modo che parta ogni minuto)
@aiocron.crontab('* * * * *')
def report_generator():
    """
    Questo scheduler prende inizialmente gli utenti della tabella e successivamente
    crea un task asyncrono per la generazione del report singolo, in modo che gestisca la creazione
    in multi-thread senza aspettare che finisca quello precedente
    :return:
    """
    try:
        utenti = Utenti.select()
        for utente in utenti:
            logging.info('{} : Inizio generazione report per utente id: {} nome: {}'.format(datetime.now(), utente.id, utente.nome))
            asyncio.get_event_loop().create_task(create_report(utente))
    except Exception as e:
        logging.error('Qualcosa è andato storto. Dettaglio errore: {}'.format(e.__str__()))


logging.info("Script partito correttamente.")
asyncio.get_event_loop().run_forever()
