import os
from langchain.schema import Document

# Langchain Document structure:
'''
sample_langchain_Document = Document(
    metadata={
            'source': 'Example.pdf', 
            'page': 0
            }, 
        page_content='Example content'
)
sample_langchain_Document_List = [
    Document(
        metadata={
                'source': 'Carlos_Acesso.pdf', 
                'page': 0
                }, 
            page_content="""
            Projeto-Item Carlos_Acesso, 14092017 (76 min).docx\nResponsável contato@transcricoes.com.br   –   Carlos (transcritor) Michelle
            (revisora)\nFICHA TÉCNICA\nInformações adicionais da gerência de produção\nO trabalho foi considerado de média dificuldade, acertos estimados
            em 97 por cento ou mais.\nTRANSCRIÇÃO DE ÁUDIO\nConvenções adotadas\npalavra... = alongamento vocálico, hesitação ou interrupção de ato de 
            fala.\n... palavra = continuação da fala do turno do falante que foi interrompida.\n(...) = demonstração de corte de fala considerado não 
            relevante.\n[01:46:09] = marcação de tempo [hh:mm:ss] (*)\n(hipótese) [00:00:00] = hipótese de escuta ou fonográfica 
            (o som que conseguimos entender)\n(inint) [00:00:00] = trecho ou palavra que não conseguimos compreender.\n((palavra)) = comentários do 
            transcritor.\n(*) A marcação de tempo ocorre uma vez a cada 5 linhas para cima ou para baixo caso ocorram\nmuitos (inint) ou (hipótese) 
            devidamente sinalizada com [hh:mm:ss]. Uma hipótese de escuta é\nsinalizada apenas uma vez e após sua ocorrência deixa de ser sinalizada 
            como tal.\nIdentificação de falantes\nP: Pesquisador(a)\nH1: Falante masculino\nF1: Falante feminino\n((início da transcrição))
            \nP: 
            Eu não queria perder aquela primeira informação que é  em  relação ao tempo de\ncliente... 
            \nH1: 
            Quanto tempo que o cliente demora para se pagar.
            \n \nP: 
            É.
            \nH1: 
            Está bem. Depende muito do canal de vendas. 
            \n \nP: 
            Três meses, você comentou.
            \nH1: 
            Isso. O que acontece? No nosso canal de vendas do varejo nós não ganhamos nada\nna venda do cartão de plástico. Está bem? 
            \n \nP: 
            Aham.
            \nH1: 
            Nós ganhamos dinheiro quando o cliente usar o cartão. Por que eu digo isso?\nPorque nós vendemos através de um distribuidor, então o preço
            do cartão lá no varejo é\n14,90. Dos 14,90 vamos pagar imposto, mais ou menos 10 por cento arredondando, e\nnós pagamos uma comissão de 80
            por cento para o distribuidor. Então, dos 14,90 a\nAcesso fica líquido de um real 50 arredondando. O plástico custa para nós colocá-lo 
            lá\nna gôndola, só a produção e gráfica e etcétera... ele custa mais ou menos três e 50 a\nquatro reais dependendo se tem muita pedra ou não. Então, eu gastei quatro reais e\nfaturei 1,50 e então hoje nós temos esse gap de mais ou menos seria a diferença. Então
            """
    ), 

    Document(
        metadata={
        'source': 'Carlos_Acesso.pdf', 
        'page': 1
        }, 
        page_content="""
        para nós lucrar com aquele cliente, ele tem que pelo menos ficar vivo no primeiro mês.\nUm cliente deixa para nós hoje uma média de lucro por mês de três reais então três reais\nmais um e 50 no primeiro mês ele vira break evento. Então eu preciso que ele fique pelo\nmenos dois meses a três para ele valer a pena. No canal e-commerce que nós vendemos\no cartão, você depois entra no site do Acesso, você cadastra e pede o teu cartão lá,\ngeralmente se a pessoa bota mais de 100 reais no cartão, nós não cobramos os 14,90\nporque aquele valor eu não divido com distribuidor, você me entendeu? Eu tenho que\ncobrar  os  14,90  porque  eu  tenho  que  dividir  o  dinheiro  para  o  distribuidor.  E  o\ndistribuidor, a minha concorrência hoje... 
        \n \nP: 
        Nossa, vou pegar um desses para pagar a minha empregada.
        \nH1: 
        É, pode, na internet ali é muito bom. Internet na verdade é melhor porque o cartão é\nchipado. A diferença é o que? O tarja, aqui no Brasil, as pessoas não estão muito\nacostumados a usá-lo porque o Brasil na verdade, no segmento de cartões ele ficou à\nfrente da Europa e dos Estados Unidos por causa de fraude. Então, cartão chipado veio\nno Brasil há mais ou menos nove, dez anos atrás. E a minha primeira conta bancária\naqui no Brasil é em 2009 e já era chipado por questão de fraude e clonagem. Então... 
        \n \nP: 
        Os norte americanos estão chipando agora.
        \nH1: 
        Chipou o ano passado. Minha conta bancária que eu tenho nos Estados Unidos, eles\nme pediram o ano passado para destruir o meu antigo cartão e que eu iria receber o novo\npelo correio. Estou falando de janeiro e fevereiro de 2016 versus 2007. Então há nove\nanos atrás. O que acontece? Nos Estados Unidos é... as pessoas especialmente quem\ntrabalha  no  comércio  estão  muito  acostumados  a  trabalhar  na  tarja.  Então  não  é\nautomático, pega o cartão e passa. Passa, passa. Aqui no Brasil, não. O que aconteceu?\nVocê vai no mercado e a pessoa já não entende que seu cartão não tem chip. Então você\nfala “não, tem que passar” e aí, na hora de passar, ele pede o código de segurança que é\no número que está atrás do cartão. Aí geralmente a pessoa se confunde com isso sendo o\nseu PIN para validar a transação, entendeu? E aí, a pessoa bota lá a senha aí fala “deu\nerro”. E dá aqueles três, cinco segundos que você acha que está a uma hora na caixa que\nestá todo mundo te olhando e fala “ah, as pessoas vão pensar que eu não tenho dinheiro\ne que por isso que o cartão não passou”. Mas na verdade é que as pessoas não estão\nacostumadas a usar e quando pede o código é o código CVC que está atrás do cartão e\nnão PIN de segurança. 
        \n \nP: 
        Tá. 
        \nH1: 
        Era seis. 
        \n \nP: 
        Entendi. Já teve uma evolução só de mudar esses...?
        \nH1:
        Isso. Porque nos seis meses era o cara que comprou descartável. Comprei, deixei,\nentendeu? Agora com essa mudança já foi para dez, a ideia que é que chegue a 15\nmeses, 18 meses. 
        \n \nP: 
        Uhum. Então, certo. Muito bom. Posso encerrar? \n((fim da transcrição)) 
        """
    )
]

ACCESS: https://python.langchain.com/docs/how_to/document_loader_pdf/

TO PRINT: print(document_name[10].metadata['source'])
'''

def extract_text_content_from_langchain_Document_List(langchain_Document_data_list):
    text_content = []
    for doc in langchain_Document_data_list:
        if isinstance(doc, Document):  # Check if it's a Document object
            source = os.path.basename(doc.metadata.get('source', 'Unknown'))
            page = doc.metadata.get('page', 'Unknown')
            content = f"## Fonte: {source} \n ## Pag.: {page} \n{doc.page_content}\n *************************************** \n "
            text_content.append(content)
        else:
            print(f"Warning: Non-Document object found in the list: {doc}")
            text_content.append(f"***non Document object*******\n{doc}\n\n***end of non Document object*******")
    
    return "\n".join(text_content) # it is a string
'''
# Example usage:
sample_langchain_Document_List = [
    Document(
        metadata={
                'source': 'Carlos_Acesso.pdf', 
                'page': 0
                }, 
            page_content="""
            Projeto-Item Carlos_Acesso, 14092017 (76 min).docx\nResponsável contato@transcricoes.com.br   –   Carlos (transcritor) Michelle
            (revisora)\nFICHA TÉCNICA\nInformações adicionais da gerência de produção\nO trabalho foi considerado de média dificuldade, acertos estimados
            em 97 por cento ou mais.\nTRANSCRIÇÃO DE ÁUDIO\nConvenções adotadas\npalavra... = alongamento vocálico, hesitação ou interrupção de ato de 
            fala.\n... palavra = continuação da fala do turno do falante que foi interrompida.\n(...) = demonstração de corte de fala considerado não 
            relevante.\n[01:46:09] = marcação de tempo [hh:mm:ss] (*)\n(hipótese) [00:00:00] = hipótese de escuta ou fonográfica 
            (o som que conseguimos entender)\n(inint) [00:00:00] = trecho ou palavra que não conseguimos compreender.\n((palavra)) = comentários do 
            transcritor.\n(*) A marcação de tempo ocorre uma vez a cada 5 linhas para cima ou para baixo caso ocorram\nmuitos (inint) ou (hipótese) 
            devidamente sinalizada com [hh:mm:ss]. Uma hipótese de escuta é\nsinalizada apenas uma vez e após sua ocorrência deixa de ser sinalizada 
            como tal.\nIdentificação de falantes\nP: Pesquisador(a)\nH1: Falante masculino\nF1: Falante feminino\n((início da transcrição))
            \nP: 
            Eu não queria perder aquela primeira informação que é  em  relação ao tempo de\ncliente... 
            \nH1: 
            Quanto tempo que o cliente demora para se pagar.
            \n \nP: 
            É.
            \nH1: 
            Está bem. Depende muito do canal de vendas. 
            \n \nP: 
            Três meses, você comentou.
            \nH1: 
            Isso. O que acontece? No nosso canal de vendas do varejo nós não ganhamos nada\nna venda do cartão de plástico. Está bem? 
            \n \nP: 
            Aham.
            \nH1: 
            Nós ganhamos dinheiro quando o cliente usar o cartão. Por que eu digo isso?\nPorque nós vendemos através de um distribuidor, então o preço
            do cartão lá no varejo é\n14,90. Dos 14,90 vamos pagar imposto, mais ou menos 10 por cento arredondando, e\nnós pagamos uma comissão de 80
            por cento para o distribuidor. Então, dos 14,90 a\nAcesso fica líquido de um real 50 arredondando. O plástico custa para nós colocá-lo 
            lá\nna gôndola, só a produção e gráfica e etcétera... ele custa mais ou menos três e 50 a\nquatro reais dependendo se tem muita pedra ou não. Então, eu gastei quatro reais e\nfaturei 1,50 e então hoje nós temos esse gap de mais ou menos seria a diferença. Então
            """
    ), 

    Document(
        metadata={
        'source': 'Carlos_Acesso.pdf', 
        'page': 1
        }, 
        page_content="""
        para nós lucrar com aquele cliente, ele tem que pelo menos ficar vivo no primeiro mês.\nUm cliente deixa para nós hoje uma média de lucro por mês de três reais então três reais\nmais um e 50 no primeiro mês ele vira break evento. Então eu preciso que ele fique pelo\nmenos dois meses a três para ele valer a pena. No canal e-commerce que nós vendemos\no cartão, você depois entra no site do Acesso, você cadastra e pede o teu cartão lá,\ngeralmente se a pessoa bota mais de 100 reais no cartão, nós não cobramos os 14,90\nporque aquele valor eu não divido com distribuidor, você me entendeu? Eu tenho que\ncobrar  os  14,90  porque  eu  tenho  que  dividir  o  dinheiro  para  o  distribuidor.  E  o\ndistribuidor, a minha concorrência hoje... 
        \n \nP: 
        Nossa, vou pegar um desses para pagar a minha empregada.
        \nH1: 
        É, pode, na internet ali é muito bom. Internet na verdade é melhor porque o cartão é\nchipado. A diferença é o que? O tarja, aqui no Brasil, as pessoas não estão muito\nacostumados a usá-lo porque o Brasil na verdade, no segmento de cartões ele ficou à\nfrente da Europa e dos Estados Unidos por causa de fraude. Então, cartão chipado veio\nno Brasil há mais ou menos nove, dez anos atrás. E a minha primeira conta bancária\naqui no Brasil é em 2009 e já era chipado por questão de fraude e clonagem. Então... 
        \n \nP: 
        Os norte americanos estão chipando agora.
        \nH1: 
        Chipou o ano passado. Minha conta bancária que eu tenho nos Estados Unidos, eles\nme pediram o ano passado para destruir o meu antigo cartão e que eu iria receber o novo\npelo correio. Estou falando de janeiro e fevereiro de 2016 versus 2007. Então há nove\nanos atrás. O que acontece? Nos Estados Unidos é... as pessoas especialmente quem\ntrabalha  no  comércio  estão  muito  acostumados  a  trabalhar  na  tarja.  Então  não  é\nautomático, pega o cartão e passa. Passa, passa. Aqui no Brasil, não. O que aconteceu?\nVocê vai no mercado e a pessoa já não entende que seu cartão não tem chip. Então você\nfala “não, tem que passar” e aí, na hora de passar, ele pede o código de segurança que é\no número que está atrás do cartão. Aí geralmente a pessoa se confunde com isso sendo o\nseu PIN para validar a transação, entendeu? E aí, a pessoa bota lá a senha aí fala “deu\nerro”. E dá aqueles três, cinco segundos que você acha que está a uma hora na caixa que\nestá todo mundo te olhando e fala “ah, as pessoas vão pensar que eu não tenho dinheiro\ne que por isso que o cartão não passou”. Mas na verdade é que as pessoas não estão\nacostumadas a usar e quando pede o código é o código CVC que está atrás do cartão e\nnão PIN de segurança. 
        \n \nP: 
        Tá. 
        \nH1: 
        Era seis. 
        \n \nP: 
        Entendi. Já teve uma evolução só de mudar esses...?
        \nH1:
        Isso. Porque nos seis meses era o cara que comprou descartável. Comprei, deixei,\nentendeu? Agora com essa mudança já foi para dez, a ideia que é que chegue a 15\nmeses, 18 meses. 
        \n \nP: 
        Uhum. Então, certo. Muito bom. Posso encerrar? \n((fim da transcrição)) 
        """
    )
]
example = extract_text_content_from_langchain_Document_List(sample_langchain_Document_List)
print(example)
print(f"\ntype: {type(example)}")
'''