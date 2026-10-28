# Perfil Python

Leia somente quando selecionado em context. Use o gerenciador, ambiente virtual,
estilo de imports e runner já adotados pelo projeto. Não migre para pytest,
uv, poetry ou outra ferramenta como efeito colateral.

Novos scripts de arquivos precisam preservar dados existentes e restringir
caminhos ao destino autorizado. Use subprocess com lista de argumentos e
shell=False quando executar programas; não use eval para comandos do perfil.
Teste invariantes observáveis, falhas e efeitos colaterais relevantes.
Para o próprio kit, o runner é unittest da biblioteca padrão.
