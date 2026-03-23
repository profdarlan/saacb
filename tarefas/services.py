# tarefas/services.py
import re
from num2words import num2words
from django.utils import timezone
import locale


TEMPLATES = {
    'despacho': """DESPACHO DE INSTAURAÇÃO DE COBRANÇA ADMINISTRATIVA DE VALORES RECEBIDOS INDEVIDAMENTE EM BENEFÍCIO

Seção de Análise e Cobrança Administrativa de Benefícios, em {data_atual}

Ref.: Processo nº {sei}
Número do Benefício: {nb}
Titular do Benefício: {nome} ( {cpf} )
Int.: {resp_l} ( {cpf_rl} )
Tarefa RCADBENEF: {tarefa_n}
Ass.: Cobrança Administrativa de Valores Recebidos Indevidamente em Benefício

O INSS, após a avaliação de que trata o art. 11 da Lei nº 10.666/2003, identificou recebimento indevido no benefício {nb}, no período de {periodo}, que perfaz o total de R$ {valor} ( {valor_ext} ) atualizado até a presente data (Discriminativo de Cálculo dos Valores - anexo), a título de {motivo}.

O processo administrativo de {motivo}, após o devido processo legal, confirmou a irregularidade e concluiu pelo parecer definitivo acerca da responsabilização pelo {tipo_cred} em desfavor de {resp_pag}.""",
    'despacho_tutela': """DESPACHO DE INSTAURAÇÃO DE COBRANÇA ADMINISTRATIVA DE VALORES RECEBIDOS INDEVIDAMENTE EM BENEFÍCIO

Seção de Análise e Cobrança Administrativa de Benefícios, em {data_atual}

Ref.: Processo nº {sei}
Número do Benefício: {nb}
Titular do Benefício: {nome} ( {cpf} )
Int.: {resp_l} ( {cpf_rl} )
Tarefa RCADBENEF: {tarefa_n}
Ass.: Cobrança Administrativa de Valores Recebidos em função de Antecipação de Tutela Cassada/Reformada

O INSS, após a avaliação de que trata o art. 11 da Lei nº 10.666/2003, identificou recebimento indevido no benefício {nb}, no período de {periodo}, que perfaz o total de R$ {valor} ( {valor_ext} ) atualizado até a presente data (Discriminativo de Cálculo dos Valores - anexo), a título de {motivo}.

Conforme Despacho com Força Executória encaminhado {historico}.""",
    'analise_defesa': """Seção de Análise e Cobrança Administrativa de Benefícios, em {data_atual}


Ref.: Processo nº {sei}

Número do Benefício: {nb}

Titular do Benefício: {nome} ( {cpf} )

Tarefa RCADBENEF: {tarefa_n}

Ass.: Cobrança Administrativa de Valores Recebidos Indevidamente em Benefício



O INSS, após a avaliação de que trata o art. 11 da Lei nº 10.666/2003, identificou recebimento indevido no benefício {nb}, no período de {periodo}, que perfaz o total de R$ {valor} ({valor_ext}), a título de {motivo}.

O processo administrativo de Apuração do benefício referenciado, após o devido processo legal, confirmou a irregularidade e concluiu pelo parecer definitivo acerca da responsabilização pelo {tipo_cred} em desfavor de {nome} ( {cpf} )

Esgotadas as possibilidades de recurso na via administrativa em relação ao mérito da ocorrência ou irregularidade que deu causa ao recebimento indevido do benefício, foi emitida notificação de cobrança administrativa, facultando ao (à) interessado(a) o prazo de 30 dias para apresentação de defesa contra a cobrança, relativo aos valores, forma de cálculo, correção monetária e eventual incidência de acréscimos legais.

Houve ciência por parte do interessado quanto à notificação referenciada em {oficio1}, comprovada por meio do {AR1} .

Em sua defesa, o(a) interessado(a) alega, em síntese, que: {obs1} .

{obs2}

Da análise das alegações do interessado, verificamos que {es_conc}.

Ante o exposto acatamos a defesa contra a cobrança na forma e no mérito a julgamos {fim_conc}.""",
    'oficio_recurso': """O INSS, após avaliação do art. 11 da Lei nº 10.666/2003, identificou recebimento indevido no benefício {nb}, no período {periodo}, totalizando R$ {valor}({valor_ext}), a título de {motivo}. Decorrido o prazo regulamentar {es_conc_of}.
V. Sa. deverá quitar o débito em até 60 dias, por Guia, parcelamento ou consignação em folha/benefício; ou interpor recurso ao Conselho de Recursos do Seguro Social em até 30 dias, pelo telefone 135 ou pelo site/aplicativo Meu INSS.
O acesso ao dossiê, emissão da Guia, demonstrativo e solicitação de parcelamento podem ser feitos no Meu INSS, no Protocolo {tarefa_n}, ou por agendamento do serviço “CUMPRIMENTO DE EXIGÊNCIA” pelo 135 ou pelo aplicativo. No atendimento presencial, apresente esta notificação.
A falta de quitação ou adesão acarretará consignação compulsória (se houver benefício ativo), cobrança judicial, inscrição em Dívida Ativa e inclusão no CADIN""",
    'oficio_defesa_tutela': """O INSS, identificou recebimento indevido no benefício {nb}, entre {periodo}, que perfaz o total de R$ {valor} ({valor_ext}), valor atualizado até a presente data. Devido a {motivo}({procj}), e determinação para cobrança administrativa, nos termos do Tema 692(STJ).
O interessado poderá apresentar defesa a partir da ciência da notificação, contestando valores, cálculos e encargos. Para pagamento, há três opções:
a) quitar a guia de recolhimento em até 60 (sessenta) dias;
b) solicitar parcelamento do débito por meio de Termo de Parcelamento;
c) autorizar consignação em folha de pagamento e/ou benefício.
A apresentação de defesa, bem como o acesso ao dossiê eletrônico, acesso a guia, demonstrativos e solicitação de parcelamento, poderá ser realizada pelo site ou aplicativo Meu INSS, no serviço "Cobrança Administrativa - MOB", sob o Protocolo {tarefa_n}, ou presencialmente, mediante agendamento pelo 135. A ausência de quitação ou de adesão às modalidades de pagamento poderá resultar em consignação compulsória, cobrança judicial e inclusão em cadastro de inadimplentes - CADIN.""",
    'oficio_defesa': """O INSS, após avaliação, identificou recebimento indevido no benefício {nb}, entre {periodo}, que perfaz o total de R$ {valor} ({valor_ext}), valor atualizado até a presente data. Considerando a existência de {motivo}, e após o devido processo legal, a irregularidade, concluindo-se pelo parecer definitivo acerca da responsabilização pelo {tipo_cred} em desfavor de {resp_pag}.
O interessado poderá apresentar defesa a partir da ciência da notificação, contestando valores, cálculos e encargos. Para pagamento, há três opções:
a) quitar a guia de recolhimento em até 60 (sessenta) dias;
b) solicitar parcelamento do débito por meio de Termo de Parcelamento;
c) autorizar consignação em folha de pagamento e/ou benefício.
A apresentação de defesa, bem como o acesso ao dossiê eletrônico, acesso a guia, demonstrativos e solicitação de parcelamento, poderá ser realizada pelo site ou aplicativo Meu INSS, no serviço "Recuperação de Crédito e Cobrança Administrativa - RCADBENEF", sob o Protocolo {tarefa_n}, ou presencialmente, mediante agendamento pelo 135. A ausência de quitação ou de adesão às modalidades de pagamento poderá resultar em consignação compulsória, cobrança judicial e inclusão em cadastro de inadimplentes - CADIN.""",
'analise_tutela': """Seção de Análise e Cobrança Administrativa de Benefícios, em {data_atual}

Ref.: Processo nº {sei}
Processo Judicial nº {procj}
Número do Benefício: {nb}
Titular do Benefício: {nome} ( {cpf} )
Tarefa RCADBENEF: {tarefa_n}
Ass.: Cobrança Administrativa de Valores Recebidos em Razão de Antecipação de Tutela Cassada/Reformada

O INSS identificou a obrigatoriedade de reposição de valores recebidos no benefício {nb}, no período de {periodo}, totalizando R$ {valor} ({valor_ext}), decorrentes de antecipação de tutela concedida no processo judicial nº {procj}, a título de {motivo}.

Considerando a natureza precária da decisão judicial que fundamentou o pagamento e sua posterior cassação/reforma pelo juízo competente, restou confirmada a responsabilidade pelo {tipo_cred} em desfavor de {nome} ( {cpf} ), conforme entendimento firmado pelo STJ no Tema Repetitivo 692.

Esgotadas as instâncias judiciais quanto à obrigação de devolver os valores, foi emitida notificação de cobrança administrativa, facultando ao (à) interessado(a) o prazo de 30 dias para apresentação de defesa contra a cobrança, relativo aos valores, forma de cálculo, correção monetária e eventual incidência de acréscimos legais.

Houve ciência por parte do interessado quanto à notificação referenciada em {oficio1}, comprovada por meio do {AR1} .

Em sua defesa, o(a) interessado(a) alega, em síntese, que: {obs1} .

{obs2}

Da análise das alegações do interessado, verificamos que {es_conc}.

Ante o exposto, a defesa contra a cobrança, na forma e no mérito, é julgada {fim_conc}.""",

}

def gerar_texto_documento(tarefa, tipo_doc):
    # Normalização do valor (aceita 26.951,72 / 26.951.72 / 26951.72)
    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR.utf8') # Linux/Docker
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252') # Windows
        except locale.Error:
            pass # Caso o sistema não tenha o pacote de idiomas instalado
    bruto = str(tarefa.valor or "").strip()

    if not bruto:
        valor_monetario = 0.0
    else:
        import re
        # mantém só dígitos, vírgula e ponto
        bruto = re.sub(r'[^0-9,\.]', '', bruto)
        # remove separador de milhar
        bruto = bruto.replace('.', '')
        # troca vírgula por ponto (se houver)
        bruto = bruto.replace(',', '.')
        # agora está em formato 26951.72
        valor_monetario = float(bruto)

    v_int = int(valor_monetario)
    v_cent = int(round((valor_monetario - v_int) * 100))

    from num2words import num2words
    extenso = f"{num2words(v_int, lang='pt-br')} reais"
    if v_cent > 0:
        extenso += f" e {num2words(v_cent, lang='pt-br')} centavos"
    
    contexto = {
            'data_atual': timezone.now().strftime('%d de %B de %Y'),
            'sei': tarefa.sei_n,
            'nb': tarefa.nb1,
            'procj': tarefa.procj or "***VERIFICAR NÚMERO DO PROCESSO JUDICIAL***",  # Inclusão da nova variável
            'oficio1': tarefa.oficio1.strftime('%d/%m/%Y') if tarefa.oficio1 else "**VERIFICAR DATA DE CIÊNCIA DO OFÍCIO COBRANÇA**",
            'AR1': tarefa.AR1,
            'obs1': tarefa.obs1,
            'obs2': tarefa.obs2 if tarefa.obs2 else "",
            'es_conc_of': tarefa.es_conc if tarefa.es_conc else "***VERIFICAR CONCLUSÃO DA ANÁLISE***",
            'es_conc': tarefa.es_conc.conc_exp if tarefa.es_conc else "***VERIFICAR CONCLUSÃO DA ANÁLISE***",
            'fim_conc': tarefa.es_conc.fim if tarefa.es_conc else "***",
            'status': tarefa.status,
            'nome': tarefa.nome_interessado,
            'cpf': tarefa.CPF,
            'resp_l': tarefa.responsavel or "Não informado",
            'cpf_rl': tarefa.CPF_R or "Não informado",
            'tarefa_n': tarefa.tarefa_n,
            'periodo': tarefa.Periodo_irregular,
            'valor': tarefa.valor,
            'valor_ext': extenso,
            'motivo': tarefa.nome_serv or "irregularidade constatada", # Usando campo Fatos como motivo
            'tipo_cred': tarefa.tip_con or "crédito devido",      # Usando campo Tipo Conclusão
            'historico': tarefa.historico or "***VERIFICAR HISTÓRICO DA TAREFA E DESCREVER O FUNDAMENTO DO DÉBITO***",
            'resp_pag': tarefa.responsavel if tarefa.responsavel else tarefa.nome_interessado,
        }
    template = TEMPLATES.get(tipo_doc, "Template não encontrado.")
    return template.format(**contexto)
