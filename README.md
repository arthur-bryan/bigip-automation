# instala dependencias
python3 -m pip install requirements.txt

# seta variaveis de ambiente (exemplo abaixo é no linux)
export BIGIP_USER=seu_usuario_no_bigip
export BIGIP_PASS=sua_senha

# executa o script para ingressar/remover servidores da AWS no pool do Mobilidade
python3 crise-mobilidade-renner-aws-bigip.py

# executa o script para ingressar/remover servidores da Azure no pool do Mobilidade
python3 crise-mobilidade-renner-aws-bigip.py
