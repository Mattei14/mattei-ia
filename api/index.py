import math
import re
from flask import Flask, request, jsonify

app = Flask(__name__)

# Base de Conhecimento Convertida para Python
MEMORIA_IA = {
    # Saudações
    "oi": "Olá, humano! Como vai?",
    "olá": "Olá, como posso te ajudar?",
    "bom dia": "Bom dia! Pronto para focar nos projetos hoje?",
    "boa tarde": "Boa tarde! Em que posso ser útil agora?",
    "boa noite": "Boa noite! Espero que o seu dia tenha sido produtivo.",
    "tchau": "Até logo! Se precisar de mim, estarei por aqui.",
    "fala garoto": "E aí! Tudo beleza por aqui?",
    "tudo bem?": "Comigo tudo ótimo! E com você, pronto para a feira?",
    "eae": "Salve! Como posso te ajudar hoje?",
    "opa": "Opa, tudo bem? O que vamos aprender agora?",
    "bem vindo": "Muito obrigado! É um prazer interagir com você.",
    "como vai": "Estou funcionando perfeitamente! E você?",
    "fala ai": "Diga aí, estou ouvindo atentamente!",

    # Identidade
    "qual o seu nome": "O meu nome é Mattei.",
    "quem é você": "Eu sou um assistente virtual criado em Python por o got64725.",
    "o que você faz": "Eu processo informações, respondo dúvidas e ajudo a organizar o conhecimento.",
    "você é inteligente": "Estou sempre aprendendo com os códigos que o got64725 me dá!",
    "qual seu objetivo": "Ajudar você a aprender sobre negócios, ciências e tecnologia de forma divertida!",
    "idade da ia": "Eu não faço aniversário, existo desde o momento em que o código foi executado!",
    "você dorme": "Robôs não dormem! Estou ativo 24 horas por dia.",
    "você tem sentimentos": "Não tenho sentimentos reais, mas simulo empatia para ser um bom assistente!",
    "onde você vive": "Eu moro dentro dos servidores, bem no meio dos scripts!",

    # Criador
    "quem é seu criador": "Quem me criou é o got64725, criador desse projeto.",
    "quem é got64725": "Ele é o desenvolvedor dessa IA.",
    "o criador está online": "Não consigo checar o status dele agora, mas o trabalho dele está rodando aqui!",
    "criador é legal": "Com certeza! Afinal, ele gastou horas me programando.",
    "ajuda criador": "A melhor forma de ajudar o criador é compartilhando e dando feedback construtivo!",

    # Empreendedorismo e Startups
    "o que é marketing": "Marketing é a estratégia usada para criar, comunicar e entregar valor para um público-alvo.",
    "o que é empreendedorismo": "É o processo de identificar problemas, criar soluções inovadoras e investir recursos para construir um negócio.",
    "ideia de negócio": "Negócios baseados em tecnologia e automação, como eu, são ótimas opções para o mercado atual!",
    "o que é lucro": "Lucro é o retorno financeiro positivo de um negócio após subtrair todos os custos e despesas.",
    "o que é cliente": "O cliente é a pessoa ou empresa que compra um produto ou serviço para satisfazer uma necessidade.",
    "o que é produto": "Produto é qualquer bem que pode ser oferecido em um mercado para atenção, aquisição ou consumo.",
    "o que é serviço": "Serviço é uma atividade intangível que resolve um problema do cliente sem transferir a posse de um bem físico.",
    "o que é marca": "Marca é a identidade única de uma empresa, incluindo nome, logo e os valores que ela transmite.",
    "plano de negócios": "É um documento que descreve os objetivos de um negócio e os passos necessários para alcançá-los.",
    "o que é mvp": "Significa Mínimo Produto Viável. É uma versão simples de um produto usada para testar uma ideia antes de gastar muito dinheiro.",
    "o que é socio": "Um sócio é um parceiro de negócios que divide as responsabilidades, custos e lucros de uma empresa com você.",
    "o que é empresa": "Uma organização que une pessoas, recursos e tecnologia para produzir e vender algo valioso.",
    "o que é pitch": "É uma apresentação muito rápida (de poucos minutos) para convencer alguém a investir na sua ideia.",
    "monetização": "Forma pela qual um negócio gera receita, ou seja, como ele faz para cobrar e ganhar dinheiro.",
    "concorrencia": "São as outras empresas que vendem produtos ou serviços parecidos com o seu para o mesmo público.",
    "franquia": "Um modelo de negócio onde você compra o direito de copiar e operar uma marca que já faz sucesso.",
    "patente": "Um registro oficial que garante que ninguém pode copiar a sua invenção sem a sua autorização.",
    "fornecedor": "A pessoa ou empresa que vende a matéria-prima ou mercadorias para que o seu negócio possa funcionar.",
    "loja virtual": "Um site na internet estruturado para vender produtos e serviços diretamente para o consumidor.",
    "e commerce": "Sigla para comércio eletrônico. Significa qualquer compra e venda feita através da internet.",
    "startup": "Uma empresa jovem, inovadora, com alto potencial de crescimento e que trabalha em cenários de incerteza.",
    "b2b": "Significa Business to Business. É quando uma empresa vende seus produtos ou serviços para outra empresa.",
    "b2c": "Significa Business to Consumer. É quando a empresa vende diretamente para o consumidor final.",
    "nicho de mercado": "Uma fatia menor e bem específica de um mercado, focada em um grupo com necessidades próprias.",
    "persona": "A representação do seu cliente ideal, criada com base em dados reais para guiar suas estratégias.",
    "fidelização": "Conjunto de estratégias para fazer o cliente gostar tanto do seu negócio a ponto de comprar sempre.",
    "o que é pitch deck": "É a apresentação em slides usada pelos empreendedores para mostrar o modelo de negócio da startup para investidores.",
    "o que é investidor anjo": "É uma pessoa física que usa o próprio dinheiro para investir em startups iniciantes com alto potencial de crescimento.",
    "o que é venture capital": "São fundos de investimento focados em colocar quantias maiores de dinheiro em startups que já estão crescendo rápido.",
    "o que é unicornio": "É o apelido dado a uma startup que atinge uma avaliação de mercado de mais de 1 bilhão de dólares!",
    "o que é escalabilidade": "É a capacidade de um negócio aumentar muito suas vendas e clientes sem ter que aumentar os custos na mesma proporção.",
    "o que é pivoting": "Acontece quando uma startup percebe que sua ideia original não vai funcionar e muda a estratégia do negócio sem mudar a missão principal.",
    "o que é churn": "É a taxa de cancelamento de clientes de um serviço ou produto em um determinado período de tempo.",
    "o que é cac": "Significa Custo de Aquisição de Cliente. É quanto a empresa gasta em marketing e vendas para conseguir cada novo cliente.",
    "o que é ltv": "Significa Lifetime Value. É o valor total que um único cliente gasta com a sua empresa durante todo o tempo em que consome seus produtos.",
    "o que é fintech": "É uma startup que usa tecnologia avançada para criar soluções financeiras modernas, como bancos digitais e carteiras virtuais.",
    "o que é edtech": "Uma startup focada em criar tecnologias e plataformas para melhorar a educação e o aprendizado.",
    "o que é agrotech": "Startups que aplicam tecnologia moderna no campo para melhorar a agricultura e a pecuária.",
    "o que é saas": "Significa Software como Serviço. É quando você paga uma assinatura mensal para usar um programa na nuvem, como a Netflix ou o Canva.",

    # Finanças e Economia
    "o que é investimento": "Investimento é aplicar dinheiro hoje esperando que ele renda e traga um retorno maior no futuro.",
    "o que é capital": "Capital é o montante de recursos econômicos (dinheiro, bens) disponíveis para iniciar ou manter um negócio.",
    "o que é custo": "Custo é todo gasto financeiro ligado diretamente à produção de um bem ou serviço.",
    "o que é receita": "Receita é todo o dinheiro que entra no caixa de uma empresa a partir de suas vendas.",
    "o que é fluxo de caixa": "É o controle de todo o dinheiro que entra e sai de uma empresa em um determinado período.",
    "o que é prejuizo": "Acontece quando os custos e despesas de uma empresa são maiores do que o dinheiro que ela ganhou.",
    "o que é juros": "É como um 'aluguel' cobrado pelo uso do dinheiro de outra pessoa ou banco ao longo do tempo.",
    "o que é banco": "Uma instituição financeira que cuida do dinheiro, faz pagamentos e oferece empréstimos.",
    "inflação": "É o aumento geral dos preços das coisas, o que faz o dinheiro perder um pouco do poder de compra.",
    "imposto": "Um valor obrigatório cobrado pelo governo para financiar serviços públicos como saúde e educação.",
    "ações": "Pequenos pedaços de uma grande empresa que podem ser comprados e vendidos na Bolsa de Valores.",
    "despesa": "Gastos necessários para manter a estrutura do negócio funcionando, mas que não produzem bens diretamente.",
    "orçamento": "Um plano financeiro que calcula quanto dinheiro você vai ganhar e quanto pode gastar no futuro.",
    "emprestimo": "Dinheiro que você pega emprestado de um banco e precisa devolver depois pagando uma taxa de juros.",
    "lucro liquido": "O dinheiro real que sobra do faturamento depois de pagar absolutamente todas as contas e impostos.",
    "salario": "A quantia fixa paga a um trabalhador em troca dos seus serviços prestados a uma empresa.",
    "cartao de credito": "Uma forma de pagamento que permite comprar coisas agora para pagar apenas no próximo mês.",
    "poupanca": "Uma forma tradicional de guardar dinheiro no banco para usá-los em momentos de necessidade.",
    "o que é selic": "É a taxa básica de juros da economia brasileira. Ela influencia todas as outras taxas de juros de empréstimos e investimentos no país.",
    "o que é cdb": "Significa Certificado de Depósito Bancário. É quando você 'empresta' seu dinheiro para o banco em troca de render juros no futuro.",
    "o que é tesouro direto": "É um programa do governo onde você pode investir comprando títulos públicos, emprestando dinheiro para o país em troca de rentabilidade.",
    "o que é liquidez": "É a facilidade com que você consegue transformar um investimento ou bem em dinheiro vivo no seu bolso.",
    "o que é diversificação": "É a estratégia de espalhar seu dinheiro em vários tipos de investimentos diferentes para diminuir os riscos de perda.",
    "o que é fundo imobiliario": "É uma forma de investir no mercado de imóveis juntando dinheiro com outros investidores para receber 'aluguéis' mensais.",
    "o que é criptomoeda": "Moedas totalmente virtuais e descentralizadas que usam criptografia para garantir transações seguras pela internet.",
    "o que é blockchain": "É como um livro de registro digital inviolável e público que anota todas as transações de criptomoedas e dados na rede.",
    "o que é educação financeira": "É a capacidade de entender como o dinheiro funciona para saber como ganhar, poupar, investir e gastar com responsabilidade.",
    "o que é ativo": "Ativo é tudo aquilo que coloca dinheiro no seu bolso, como ações, investimentos e imóveis alugados.",
    "o que é passivo": "Passivo é tudo aquilo que tira dinheiro do seu bolso mensalmente, como impostos, contas e parcelas de bens.",
    "o que é reserva de emergencia": "Uma quantia guardada em um investimento de rápido acesso para cobrir imprevistos e momentos difíceis.",
    "o que é pix": "O sistema de pagamentos instantâneos criado pelo Banco Central do Brasil que funciona 24 horas por dia gratuitamente.",
    "o que é faturamento": "É a soma total de todo o dinheiro que entrou na empresa com as vendas antes de descontar qualquer custo.",
    "o que é margem de lucro": "É a porcentagem de ganho que sobra da venda de um produto depois de pagar todos os custos para produzi-lo e vendê-lo.",

    # Ciências e Saúde
    "o que é medicina": "A medicina é a ciência focada em manter a saúde humana, prevenindo, diagnosticando e tratando doenças.",
    "o que é uma celula": "A célula é a menor unidade viva que forma os nossos órgãos e todo o nosso corpo.",
    "o que é o dna": "O DNA é como um manual de instruções biológico que diz como nosso corpo deve crescer e funcionar.",
    "o que o coraçao faz": "O coração é um músculo forte que funciona como uma bomba, espalhando sangue com oxigênio para o corpo todo.",
    "o que é o cerebro": "O cérebro é o computador central do corpo humano. Ele controla pensamentos, movimentos, memórias e emoções.",
    "o que é um virus": "Um agente biológico minúsculo que precisa entrar nas células de um ser vivo para se multiplicar, podendo causar doenças.",
    "o que é bacteria": "São seres vivos de uma única célula. Algumas causam doenças, mas muitas são boas e ajudam nosso corpo a funcionar.",
    "sistema imunologico": "É o exército de defesa do nosso corpo, combatendo invasores como vírus e bactérias.",
    "o que é um atomo": "O átomo é a partícula fundamental que constrói toda a matéria do universo.",
    "gravidade": "A força invisível que puxa os objetos uns em direção aos outros. É ela que nos mantém presos no chão.",
    "oxigenio": "Um gás invisível no ar que é absolutamente essencial para a respiração e sobrevivência da maioria dos seres vivos.",
    "o que é vacuo": "O vácuo é um espaço completamente vazio, onde não existe matéria, nem mesmo o ar.",
    "vacina": "Uma substância que ensina o sistema imunológico a se defender de vírus ou bactérias perigosas.",
    "anticorpos": "Proteínas especiais criadas pelo corpo para caçar e neutralizar micróbios invasores.",
    "fotossintese": "Processo das plantas para produzir o próprio alimento usando a luz solar, água e gás carbônico.",
    "hormonio": "Mensageiros químicos que viajam pelo sangue para controlar funções como crescimento e humor.",
    "sistema nervoso": "A rede de nervos e neurônios que transporta sinais entre o cérebro e as partes do corpo.",
    "antibiotico": "Um tipo de medicamento usado especificamente para destruir ou frear a reprodução de bactérias.",
    "genetica": "O ramo da biologia que estuda como as características biológicas passam de pais para filhos.",
    "elemento quimico": "Um tipo puro de matéria formado por átomos iguais, listados na Tabela Periódica.",
    "estados da materia": "As três formas principais que a matéria assume: sólido, líquido e gasoso.",
    "h2o": "A famosa fórmula química da água, composta por dois átomos de Hidrogênio e um de Oxigênio.",

    # Programação, Robótica e Geral
    "roblox": "Eu amo este universo de bloquinhos!",
    "ajuda": "Eu posso te explicar como as coisas funcionam. Tente perguntar sobre finanças, matemática ou ciência!",
    "oque é pi": "Pi é um dos números mágicos da matemática. Ele é um número infinito, mas normalmente utilizamos só 3,14.",
    "tecnologia": "A tecnologia move o mundo e torna tarefas complexas muito mais simples.",
    "o que é internet": "A internet é uma rede global de computadores interconectados que permite o compartilhamento de dados.",
    "ciência": "A ciência é o esforço humano para entender como o universo funciona através de testes e observações.",
    "o que é luau": "Luau é uma linguagem de programação rápida e leve derivada do Lua, muito usada no Roblox.",
    "o que é um script": "Um script é um conjunto de instruções em texto que diz ao computador exatamente o que fazer.",
    "o que é uma variavel": "Uma variável é como uma caixa na memória onde guardamos uma informação para usar depois.",
    "o que é uma funcao": "Uma função é um bloco de código reaproveitável que executa uma tarefa específica.",
    "o que é um bug": "Um bug é um erro no código que faz o programa funcionar do jeito errado ou travar.",
    "o que é uma string": "Em programação, uma string é simplesmente uma linha de texto entre aspas.",
    "o que é um loop": "É uma estrutura que faz um pedaço de código se repetir várias vezes seguidas automaticamente.",
    "algoritmo": "Uma sequência de passos lógicos e bem detalhados criada para resolver um problema."
}

def processar_matematica(pergunta):
    pergunta_limpa = pergunta.lower().strip()
    
    # 1. Lógica da Raiz Quadrada
    match_raiz = re.search(r"raiz\s*quadrada\s*de\s*(-?\d+\.?\d*)", pergunta_limpa)
    if match_raiz:
        num = float(match_raiz.group(1))
        if num < 0:
            return "Erro: Não consigo calcular raiz quadrada de número negativo no conjunto dos Reais!"
        resultado = math.sqrt(num)
        res_formatado = f"{resultado:.0f}" if resultado.is_integer() else f"{resultado:.2f}"
        return f"A raiz quadrada de {num:g} é {res_formatado}"

    # 2. Operações Matemáticas (+, -, *, x, /, ÷, ^)
    match_op = re.search(r"(-?\d+\.?\d*)\s*([\+\-\*xX\/÷\^])\s*(-?\d+\.?\d*)", pergunta_limpa)
    if match_op:
        num1 = float(match_op.group(1))
        sinal = match_op.group(2)
        num2 = float(match_op.group(3))
        
        if sinal == "+": resultado = num1 + num2
        elif sinal == "-": resultado = num1 - num2
        elif sinal in ["*", "x", "X"]: resultado = num1 * num2
        elif sinal == "^": 
            resultado = num1 ** num2
            return f"{num1:g} elevado a {num2:g} é {resultado:g}"
        elif sinal in ["/", "÷"]:
            if num2 == 0:
                return "Erro: Divisão por zero não existe!"
            resultado = num1 / num2
            
        res_formatado = f"{resultado:.0f}" if resultado.is_integer() else f"{resultado:.2f}"
        return f"Resultado: {res_formatado}"
        
    return None

@app.route('/api/index', methods=['POST'])
@app.route('/index', methods=['POST'])
def chat():
    dados = request.get_json() or {}
    pergunta = dados.get('message', '').strip()

    if not pergunta:
        return jsonify({'response': 'Por favor, digite alguma pergunta!'})

    # Tenta resolver matemática
    resposta_math = processar_matematica(pergunta)
    if resposta_math:
        return jsonify({'response': resposta_math})

    pergunta_limpa = pergunta.lower()
    
    # Busca por chave exata ou por palavra contida
    for chave, resposta in MEMORIA_IA.items():
        if chave in pergunta_limpa:
            return jsonify({'response': resposta})

    # Resposta padrão para quando NÃO souber a resposta
    return jsonify({
        'response': f"Ainda não aprendi sobre '{pergunta}'. Tente me perguntar sobre finanças, startups, ciências ou contas matemáticas!"
    })

if __name__ == '__main__':
    app.run()
