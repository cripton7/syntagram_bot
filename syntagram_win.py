from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments import lexers
import imgkit
import random
import string
import telebot


TOKEN = 'xxxxxxxxxx:xxxxxxxxxxxxxxxxxxxxxx'


def random_name():
    # generate a random file name
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    size = random.randint(8, 12)
    return ''.join(random.choice(chars) for x in range(size))


def html_to_svg(r_name, chatid):
    config_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'
    config = imgkit.config(wkhtmltoimage=config_path)
    path = r'C:\Users\Cripton\Documents\myGitProjects\syntagram\bb\{}.html'.format(
        r_name)
    output_svg = r'C:\Users\Cripton\Documents\myGitProjects\syntagram\bb\{}.svg'.format(
        r_name)
    imgkit.from_file(path, output_svg, config=config)
    output_png = r'C:\Users\Cripton\Documents\myGitProjects\syntagram\bb\{}.png'.format(
        r_name)
    imgkit.from_file(output_svg, output_png, config=config)
    photo1 = open(
        r'C:\Users\Cripton\Documents\myGitProjects\syntagram\bb\{}.png'.format(r_name), 'rb')
    photo2 = open(
        r'C:\Users\Cripton\Documents\myGitProjects\syntagram\bb\{}.png'.format(r_name), 'rb')
    tb.send_message(chatid, 'sending the highlighted code!')
    tb.send_photo(chatid, photo1)
    tb.send_document(chatid, photo2)


def write_file(file_name, output, chatid):
    with open(r'C:\Users\Cripton\Documents\myGitProjects\syntagram\html3.txt', "r") as my_code:
        beginn = my_code.read()[:-50]
        ende = my_code.read()[-50:]
        with open(r'C:\Users\Cripton\Documents\myGitProjects\syntagram\bb\{}.html'.format(file_name), "w") as final_code:
            final_code.write(beginn + output + ende)
            html_to_svg(file_name, chatid)


def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    try:
        for m in messages:
            chatid = m.chat.id
            if m.content_type == 'text':
                code = m.text
                if code == "/start":
                    tb.send_message(
                        chatid, "created by @Cripton7\nThe source code will be soon available")
                else:
                    file_name = random_name()

                    formatter = HtmlFormatter(
                        full=False, style='monokai', linenos=False)
                    lex = lexers.get_lexer_by_name("python")
                    output = highlight(code, lex, formatter)
                    tb.send_message(chatid, "please wait a second!")
                    write_file(file_name, output, chatid)

            else:
                tb.send_message(chatid, 'Please send me a valid python code!')
    except UnicodeEncodeError:
        tb.send_message(chatid, 'this is not valid!!!!!!.')


tb = telebot.TeleBot(TOKEN)
tb.set_update_listener(listener)  # register listener
tb.polling()
# Use none_stop flag let polling will not stop when get new message occur error.
tb.polling(none_stop=True)
# Interval setup. Sleep 3 secs between request new message.
tb.polling(interval=3)

while True:  # Don't let the main Thread end.
    pass
