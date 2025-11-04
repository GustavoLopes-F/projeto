import pywhatkit

# Substitua pelo seu número de teste (com DDD e +55)
numero = "+5544999999999"
mensagem = "Mensagem de teste automática ✅"

pywhatkit.sendwhatmsg_instantly(numero, mensagem, wait_time=15)
