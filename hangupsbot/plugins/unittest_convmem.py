import logging

import plugins


logger = logging.getLogger(__name__)


def _initialise(bot):
    plugins.register_admin_command(["dumpconv", "dumpusers", "resetunknownusers"])


def dumpconv(bot, event, *args):
    """dump all conversations known to the bot"""
    text_search = " ".join(args)
    lines = []
    all_conversations = bot.conversations.get().items()
    for convid, convdata in all_conversations:
        if text_search.lower() in convdata["title"].lower():
            lines.append("{} <em>{}</em> {}<br />... {} history: {} <br />... <b>{}</b>".format(
                convid, convdata["source"], len(convdata["participants"]), convdata["type"], convdata["history"], convdata["title"]))
    lines.append("<b><em>Totals: {}/{}</em></b>".format(len(lines), len(all_conversations)))
    bot.send_message_parsed(event.conv, "<br />".join(lines))


def dumpusers(bot, event, *args):
    """lists cached users records with full name, first name as unknown, and is_definitive"""
    logger.info("dumpusers started")

    if bot.memory.exists(["user_data"]):
        for chat_id in bot.memory["user_data"]:
            if "_hangups" in bot.memory["user_data"][chat_id]:
                _hangups = bot.memory["user_data"][chat_id]["_hangups"]
                if _hangups["is_definitive"]:
                    if _hangups["full_name"].upper() == "UNKNOWN" and _hangups["full_name"] == _hangups["first_name"]:
                        logger.info("dumpusers {}".format(_hangups))

    logger.info("dumpusers finished")

    bot.send_message_parsed(event.conv, "<b>please see log/console</b>")


def resetunknownusers(bot, event, *args):
    """resets cached users records with full name, first name as unknown, and is_definitive"""
    logger.info("resetunknownusers started")

    if bot.memory.exists(["user_data"]):
        for chat_id in bot.memory["user_data"]:
            if "_hangups" in bot.memory["user_data"][chat_id]:
                _hangups = bot.memory["user_data"][chat_id]["_hangups"]
                if _hangups["is_definitive"]:
                    if _hangups["full_name"].upper() == "UNKNOWN" and _hangups["full_name"] == _hangups["first_name"]:
                        logger.info("resetunknownusers {}".format(_hangups))
                        bot.memory.set_by_path(["user_data", chat_id, "_hangups", "is_definitive"], False)
    bot.memory.save()

    logger.info("resetunknownusers finished")

    bot.send_message_parsed(event.conv, "<b>please see log/console</b>")
