"use client";
import { useState } from "react";
import { 
  ShieldAlert, 
  Activity, 
  Search, 
  Building2, 
  Users, 
  Receipt, 
  TrendingUp, 
  AlertTriangle, 
  FileText, 
  CheckCircle2, 
  Scale, 
  BarChart3, 
  HelpCircle, 
  ArrowRight, 
  DollarSign, 
  BookOpen, 
  Zap, 
  Brain, 
  Briefcase,
  Mail,
  Phone,
  ArrowDown,
  Play,
  ShieldCheck,
  Download
} from "lucide-react";

// Mapeamento de Oportunidades Fiscais
const OPPORTUNITY_DETAILS: Record<string, {
  name: string;
  estimated_potential: string;
  base_legal: string;
  requirements: string[];
  action_plan: string[];
  tax_reform: string;
  icon: any;
}> = {
  tust_tusd: {
    name: "Exclusão da TUST/TUSD da Base do ICMS",
    estimated_potential: "Restituição de 5% a 12% sobre o custo acumulado de faturas de energia dos últimos 60 meses.",
    base_legal: "Tema 986 do Superior Tribunal de Justiça (STJ) - Recurso Repetitivo.",
    requirements: ["Consumidores comerciais e industriais conectados em alta tensão com faturamento em regime normal de ICMS."],
    action_plan: [
      "Solicitar o histórico de faturamento detalhado dos últimos 5 anos à distribuidora de energia elétrica.",
      "Isolar e recalcular a incidência do ICMS cobrado sobre as parcelas de TUST (transmissão) e TUSD (distribuição).",
      "Propor ação judicial ordinária para exclusão futura das tarifas e reconhecimento do indébito retroativo.",
      "Seguir para compensação de tributos correntes pós-trânsito em julgado."
    ],
    tax_reform: "O ICMS estadual será extinto e substituído pelo IBS. A cobrança do IBS incidirá de forma não cumulativa pura no consumo final, encerrando essa tese para faturas futuras. Por isso, a apuração do passivo de 5 anos de ICMS deve ser priorizada antes da migração final das alíquotas.",
    icon: Zap
  },
  icms_energia_demanda_contratada: {
    name: "ICMS sobre Demanda Contratada de Energia",
    estimated_potential: "Redução mensal média de 12% no custo de potência e restituição de 5 anos.",
    base_legal: "Súmula 391 do Superior Tribunal de Justiça (STJ).",
    requirements: ["Grandes consumidores industriais ou comerciais com contrato de demanda reservada junto à distribuidora."],
    action_plan: [
      "Levantar as contas de energia dos últimos 5 anos para comprovar o pagamento de ICMS sobre a demanda contratada total.",
      "Isolar a parcela da demanda contratada contratada mas não consumida efetivamente.",
      "Propor medida judicial com pedido de liminar para barrar a cobrança futura e reaver os valores históricos.",
      "Habilitar os créditos federais pós-sentença."
    ],
    tax_reform: "Com a fusão de impostos no IBS, a tributação incidirá apenas na potência consumida, consolidando o fim dessa modalidade e forçando a busca do indébito do ICMS histórico.",
    icon: TrendingUp
  },
  lei_do_bem: {
    name: "Lei do Bem (Incentivo Fiscal a P&D)",
    estimated_potential: "Dedução fiscal direta de 60% a 80% dos gastos em inovação tecnológica na base do IRPJ e da CSLL.",
    base_legal: "Lei nº 11.196/2005 (Capítulo III).",
    requirements: [
      "Empresas no regime tributário de Lucro Real.",
      "Realização de projetos de pesquisa tecnológica ou inovação de produto/processo.",
      "Regularidade fiscal federal ativa (CND)."
    ],
    action_plan: [
      "Elaborar o relatório de descrição técnica de todos os projetos de inovação tecnológica do ano-calendário.",
      "Mensurar financeiramente os dispêndios com salários de engenheiros, insumos dedicados e consultorias técnicas.",
      "Preencher e enviar o FORMP&D (Formulário Eletrônico) ao Ministério da Ciência, Tecnologia e Inovação (MCTI) até o prazo legal.",
      "Aplicar a exclusão fiscal extra-contábil diretamente no e-Lalur/e-Lacs da declaração anual de imposto de renda."
    ],
    tax_reform: "A Lei do Bem incide sobre impostos federais diretos (IRPJ/CSLL). Como a Reforma incide exclusivamente sobre impostos sobre o consumo (extinguindo PIS/COFINS/ICMS/ISS/IPI), os incentivos da Lei do Bem **estão integralmente mantidos**, consolidando-se como a maior blindagem de lucratividade do país.",
    icon: Brain
  },
  limitacao_base_terceiros_sistema_s: {
    name: "Limitação da Base de Terceiros (Sistema S)",
    estimated_potential: "Redução de até 1.5% na folha salarial excedente a 20 salários mínimos, com repetição retroativa média de R$ 100k a R$ 2M.",
    base_legal: "Artigo 4º da Lei nº 6.910/1981 e Tema 1079 do STJ.",
    requirements: [
      "Empresas do Lucro Real ou Presumido com folha de salários bruta superior a 20 salários mínimos nacionais.",
      "Recolhimento ativo de contribuições destinadas a terceiros (SENAI, SENAC, SESI, SESC, SEBRAE, INCRA, FNDE, etc.)."
    ],
    action_plan: [
      "Consolidar as folhas de pagamento (eSocial / DCTFWeb) dos últimos 60 meses.",
      "Efetuar o cálculo das diferenças recolhidas em excesso limitando a base ao teto de 20 salários mínimos.",
      "Ajuizar mandado de segurança com pedido de liminar para limitar os recolhimentos futuros.",
      "Habilitar la compensação administrativa no e-CAC após o trânsito em julgado."
    ],
    tax_reform: "Por incidir diretamente sobre a folha de salários, **este tributo não sofrerá alterações pela Reforma Tributária (IBS/CBS)**. Os créditos apurados e a limitação judicial conquistada continuarão vigentes e estratégicos para a folha corporativa.",
    icon: Users
  },
  recuperacao_pis_cofins_monofasico: {
    name: "Recuperação de PIS/COFINS Monofásico",
    estimated_potential: "Recuperação rápida de R$ 15k a R$ 350k para comércios varejistas de produtos elegíveis via restituição expressa.",
    base_legal: "Lei nº 10.147/2000, Lei nº 10.485/2002 e correlatas.",
    requirements: [
      "Comércios varejistas em geral (autopeças, perfumarias, farmácias, mercados, pet shops, bebidas).",
      "Empresas optantes pelo Simples Nacional ou regime Não Cumulativo."
    ],
    action_plan: [
      "Exportar os arquivos XML das notas de saída dos últimos 60 meses.",
      "Submeter à auditoria de códigos NCM (Nomenclatura do Mercosul) para identificar itens sujeitos ao regime monofásico.",
      "Segregar a receita das vendas monofásicas da base geral de faturamento no PGDAS-D.",
      "Retificar e submeter o pedido de restituição automática no portal do Simples Nacional/e-CAC (crédito em conta em até 60 dias)."
    ],
    tax_reform: "O PIS e a COFINS serão unificados na nova CBS. Embora o regime monofásico antigo seja alterado pela CBS não cumulativa, o direito de recuperar o faturamento pago em excesso nos últimos 5 anos sob o regime anterior está garantido por lei.",
    icon: Receipt
  },
  exclusao_icms_pis_cofins: {
    name: "Exclusão do ICMS da Base do PIS/COFINS",
    estimated_potential: "Redução direta de 1.5% a 3.5% sobre o custo tributário do faturamento de vendas, além de compensação retroativa.",
    base_legal: "Tema 69 do Supremo Tribunal Federal (STF) - A Tese do Século.",
    requirements: ["Empresas do Lucro Real ou Lucro Presumido com débito de ICMS destacado nas notas fiscais de venda."],
    action_plan: [
      "Obter as obrigações acessórias EFD ICMS/IPI e EFD Contribuições dos últimos 5 anos.",
      "Efetuar a apuração mensal do PIS/COFINS deduzindo o valor do ICMS destacado nas notas fiscais de saída.",
      "Retificar os SPEDs correspondentes.",
      "Entrar com pedido de compensação tributária eletrônica no e-CAC para quitar impostos federais correntes."
    ],
    tax_reform: "ICMS, PIS e COFINS serão extintos entre 2026 e 2033 com a entrada gradual do IBS/CBS. Os créditos apurados desse período continuarão válidos e utilizáveis nos termos das regras de transição da EC 132/2023.",
    icon: Scale
  }
};

const getOpportunityDetail = (id: string, defaultName: string = id) => {
  return OPPORTUNITY_DETAILS[id] || {
    name: defaultName,
    estimated_potential: "Análise sob consulta via auditoria fiscal especializada.",
    base_legal: "Legislação e normas tributárias aplicáveis.",
    requirements: ["Enquadramento fiscal sujeito a auditoria eletrônica."],
    action_plan: [
      "Mapeamento e levantamento dos arquivos digitais do período de 60 meses.",
      "Confronto de dados declarados perante o fisco.",
      "Apuração e homologação do crédito correspondente."
    ],
    tax_reform: "Sujeito às normas de transição para o IBS/CBS definidas na Emenda Constitucional da Reforma Tributária.",
    icon: HelpCircle
  };
};

// Mapeamento dos portais oficiais de todas as FAPs Estaduais do Brasil
const STATE_FAP_MAP: Record<string, { name: string; link: string }> = {
  AC: { name: "FAPAC (Fundação de Amparo à Pesquisa do Estado do Acre)", link: "https://fapac.acre.gov.br" },
  AL: { name: "FAPEAL (Fundação de Amparo à Pesquisa do Estado de Alagoas)", link: "https://fapeal.br" },
  AM: { name: "FAPEAM (Fundação de Amparo à Pesquisa do Estado do Amazonas)", link: "https://www.fapeam.am.gov.br" },
  AP: { name: "FAPEAP (Fundação de Amparo à Pesquisa do Estado do Amapá)", link: "https://fapeap.ap.gov.br" },
  BA: { name: "FAPESB (Fundação de Amparo à Pesquisa do Estado da Bahia)", link: "https://www.fapesb.ba.gov.br" },
  CE: { name: "FUNCAP (Fundação Cearense de Apoio ao Desenvolvimento Científico e Tecnológico)", link: "https://www.funcap.ce.gov.br" },
  DF: { name: "FAPDF (Fundação de Amparo à Pesquisa do Distrito Federal)", link: "https://www.fap.df.gov.br" },
  ES: { name: "FAPES (Fundação de Amparo à Pesquisa e Inovação do Espírito Santo)", link: "https://fapes.es.gov.br" },
  GO: { name: "FAPEG (Fundação de Amparo à Pesquisa do Estado de Goiás)", link: "https://fapeg.go.gov.br" },
  MA: { name: "FAPEMA (Fundação de Amparo à Pesquisa e ao Desenvolvimento Científico e Tecnológico do Maranhão)", link: "https://www.fapema.br" },
  MG: { name: "FAPEMIG (Fundação de Amparo à Pesquisa do Estado de Minas Gerais)", link: "https://fapemig.br" },
  MS: { name: "FUNDECT (Fundação de Apoio ao Desenvolvimento do Ensino, Ciência e Tecnologia do Estado de MS)", link: "https://www.fundect.ms.gov.br" },
  MT: { name: "FAPEMAT (Fundação de Amparo à Pesquisa do Estado de Mato Grosso)", link: "https://www.fapemat.mt.gov.br" },
  PA: { name: "FAPESPA (Fundação Amazônia de Amparo a Estudos e Pesquisas)", link: "https://www.fapespa.pa.gov.br" },
  PB: { name: "FAPESQ (Fundação de Apoio à Pesquisa do Estado da Paraíba)", link: "https://fapesq.rpp.br" },
  PE: { name: "FACEPE (Fundação de Amparo à Ciência e Tecnologia do Estado de Pernambuco)", link: "https://www.facepe.br" },
  PI: { name: "FAPEPI (Fundação de Amparo à Pesquisa do Estado do Piauí)", link: "http://www.fapepi.pi.gov.br" },
  PR: { name: "Fundação Araucária (FAP Paraná)", link: "https://www.fdr.pr.gov.br/Araucaria" },
  RJ: { name: "FAPERJ (Fundação de Amparo à Pesquisa do Estado do Rio de Janeiro)", link: "https://www.faperj.br" },
  RN: { name: "FAPERN (Fundação de Amparo à Pesquisa do Estado do Rio Grande do Norte)", link: "https://fapern.rn.gov.br" },
  RO: { name: "FAPERO (Fundação de Amparo à Pesquisa do Estado de Rondônia)", link: "https://fapero.ro.gov.br" },
  RR: { name: "FAPERR (Fundação de Amparo à Pesquisa do Estado de Roraima)", link: "https://faperr.rr.gov.br" },
  RS: { name: "FAPERGS (Fundação de Amparo à Pesquisa do Estado do Rio Grande do Sul)", link: "https://fapergs.rs.gov.br" },
  SC: { name: "FAPESC (Fundação de Amparo à Pesquisa e Inovação do Estado de Santa Catarina)", link: "https://fapesc.sc.gov.br" },
  SE: { name: "FAPITEC (Fundação de Apoio à Pesquisa e à Inovação Tecnológica de Sergipe)", link: "https://fapitec.se.gov.br" },
  SP: { name: "FAPESP (Fundação de Amparo à Pesquisa do Estado de São Paulo)", link: "https://fapesp.br/pipe" },
  TO: { name: "FAPT (Fundação de Amparo à Pesquisa do Estado do Tocantins)", link: "https://fapt.to.gov.br" }
};

// Dicionário completo para interatividade de todos os cartões (fomentos, reduções e inovações)
const ITEM_DETAILS: Record<string, {
  name: string;
  link: string;
  step_by_step: string[];
  suggested_projects?: string[];
  description: string;
}> = {
  // Fomentos
  "FINEP": {
    name: "FINEP (Financiadora de Estudos e Projetos)",
    link: "https://www.finep.gov.br",
    description: "Subvenção econômica federal destinada a apoiar projetos inovadores de risco tecnológico.",
    step_by_step: [
      "Acessar o portal oficial da FINEP (finep.gov.br) e verificar as chamadas públicas (editais) de Subvenção Econômica abertas.",
      "Realizar o credenciamento da empresa e da equipe de pesquisa na plataforma de submissão 'FINEP Conveniar'.",
      "Elaborar a proposta técnica, justificando detalhadamente o risco tecnológico e o ineditismo da inovação no país.",
      "Definir a planilha orçamentária do projeto (despesas elegíveis de custeio, bolsas DTI e contrapartida financeira/não financeira).",
      "Anexar certidões de regularidade tributária municipal, estadual e federal (CND) e submeter a proposta até o prazo limite."
    ],
    suggested_projects: [
      "Desenvolvimento de novos algoritmos de inteligência artificial ou processamento de linguagem natural.",
      "Criação de novos hardwares ou componentes IoT integrados a sensores avançados.",
      "Pesquisa experimental para síntese de novos insumos químicos ou biotecnológicos."
    ]
  },
  "EMBRAPII": {
    name: "EMBRAPII (Empresa Brasileira de Pesquisa e Inovação Industrial)",
    link: "https://embrapii.org.br",
    description: "Co-financiamento ágil de até 33% do valor total do projeto de inovação industrial.",
    step_by_step: [
      "Acessar o site oficial da EMBRAPII (embrapii.org.br) e localizar a lista de Unidades EMBRAPII credenciadas no seu segmento.",
      "Agendar reuniões com os pesquisadores da Unidade EMBRAPII escolhida para estruturar o plano de trabalho do projeto.",
      "Desenhar o orçamento do projeto: a EMBRAPII aporta até 1/3 sem reembolso, a empresa aporta 1/3 e a Unidade EMBRAPII aporta 1/3 (em horas de pesquisa/infraestrutura).",
      "Assinar o contrato de cooperação tecnológica tripartite diretamente com a Unidade EMBRAPII.",
      "Iniciar a execução do projeto com os laboratórios de ponta da universidade parceira."
    ],
    suggested_projects: [
      "Desenvolvimento conjunto de protótipos robóticos ou sistemas mecânicos autônomos.",
      "Refatoração de software de controle industrial para nuvem em parceria com laboratório tecnológico.",
      "Projetos de visão computacional aplicados ao controle de qualidade fabril."
    ]
  },
  "CNPq": {
    name: "CNPq (Conselho Nacional de Desenvolvimento Científico e Tecnológico)",
    link: "https://www.gov.br/cnpq/pt-br",
    description: "Financiamento em formato de bolsas de fomento para pesquisadores e técnicos aplicados ao desenvolvimento empresarial.",
    step_by_step: [
      "Verificar editais abertos no site do CNPq, especificamente nas modalidades voltadas a parcerias universidade-empresa.",
      "Identificar os pesquisadores internos ou externos com perfil acadêmico elegível (mestres/doutores).",
      "Cadastrar o projeto na Plataforma Integrada Carlos Chagas.",
      "Solicitar as cotas de bolsas específicas (DTI - Desenvolvimento Tecnológico e Industrial) para a equipe.",
      "Acompanhar os relatórios de produtividade periódicos exigidos pelo conselho."
    ],
    suggested_projects: [
      "Bolsas para doutores implementarem novos modelos preditivos de machine learning na empresa.",
      "Bolsas de pesquisa para desenvolvimento de melhorias ergonômicas ou de produto na manufatura."
    ]
  },
  "MCTI": {
    name: "MCTI (Ministério da Ciência, Tecnologia e Inovação)",
    link: "https://www.gov.br/mcti/pt-br",
    description: "Chamadas públicas temáticas governamentais com fins de incentivar o ecossistema nacional de ciência e tecnologia.",
    step_by_step: [
      "Monitorar o diário oficial e os canais de editais do MCTI para novos programas de subvenção e inovação.",
      "Acessar as plataformas parceiras autorizadas de execução do ministério (como Softex ou RNP).",
      "Registrar a empresa nos chamados temáticos de fomento de Transformação Digital e IA.",
      "Preencher e comprovar a capacidade operacional e financeira exigida pela chamada.",
      "Submeter a documentação contábil para as análises de risco do comitê avaliador."
    ],
    suggested_projects: [
      "Programas de aceleração ou coinvestimento para novos produtos digitais SaaS.",
      "Desenvolvimento de projetos focados em bioeconomia ou sustentabilidade material."
    ]
  },
  "SUFRAMA": {
    name: "SUFRAMA (Superintendência da Zona Franca de Manaus)",
    link: "https://www.gov.br/suframa/pt-br",
    description: "Isenção ou redução tributária federal e regional destinada às empresas que operam na Zona Franca de Manaus.",
    step_by_step: [
      "Cadastrar a empresa e obter a inscrição ativa perante a SUFRAMA.",
      "Apresentar Projeto Técnico-Econômico de implantação, diversificação ou atualização industrial.",
      "Obter a aprovação do Conselho de Administração da SUFRAMA (CAS).",
      "Emitir as guias de desoneração de tributos (IPI, PIS/COFINS de entrada) na compra de matérias-primas e equipamentos destinados ao polo.",
      "Comprovar os investimentos anuais de P&D (se enquadrado nas leis do polo de informática)."
    ],
    suggested_projects: [
      "Instalação de novas linhas de montagem industriais de produtos eletrônicos.",
      "Investimento regional em infraestrutura produtiva na Amazônia Ocidental."
    ]
  },
  "CAPDA": {
    name: "CAPDA (Comitê das Atividades de Pesquisa e Desenvolvimento na Amazônia)",
    link: "https://www.gov.br/suframa/pt-br/assuntos/lei-de-informatica/capda",
    description: "Gestão e incentivo fiscal compulsório de P&D para bens de tecnologia de informática e automação na região Norte.",
    step_by_step: [
      "Verificar o credenciamento de sua empresa na Lei de Informática da Zona Franca de Manaus (ZFM).",
      "Estruturar os gastos compulsórios de P&D exigidos por lei (mínimo de 5% do faturamento bruto dos bens incentivados).",
      "Cadastrar o plano de investimento de P&D na plataforma de submissão do CAPDA.",
      "Destinar os recursos para instituições de pesquisa credenciadas na Amazônia Ocidental ou em projetos internos aprovados.",
      "Enviar anualmente o Relatório de Demonstrativo de Investimento de P&D (RDA)."
    ],
    suggested_projects: [
      "Parceria de pesquisa com institutos locais (ex: INDT, CETELI) para novos softwares de controle.",
      "Desenvolvimento interno de firmware ou circuitos integrados."
    ]
  },
  "ANEEL P&D": {
    name: "ANEEL P&D (Setor Elétrico)",
    link: "https://www.gov.br/aneel/pt-br",
    description: "Incentivo e investimento tecnológico compulsório de 0,5% do faturamento líquido para o setor elétrico.",
    step_by_step: [
      "Identificar a obrigação de investimento compulsório da concessionária de energia (geradoras, transmissoras e distribuidoras).",
      "Estruturar a proposta de P&D aderente aos Temas Estratégicos regulados da ANEEL.",
      "Registrar o projeto na plataforma de monitoramento de P&D da ANEEL antes do início de sua execução.",
      "Executar em parceria com universidades e institutos de pesquisa credenciados.",
      "Submeter as planilhas financeiras e de auditoria independente final ao comitê da ANEEL."
    ],
    suggested_projects: [
      "Pesquisa em novas redes inteligentes (Smart Grids) e medidores eletrônicos de consumo.",
      "Armazenamento de energia em baterias de alta capacidade e fontes de energia renováveis."
    ]
  },
  "FAP AM": {
    name: "FAPEAM (Fundação de Amparo à Pesquisa do Estado do Amazonas)",
    link: "https://www.fapeam.am.gov.br",
    description: "Auxílios financeiros estaduais sob forma de subvenção econômica para micro, pequenas e médias empresas do Amazonas.",
    step_by_step: [
      "Acessar o site oficial da FAPEAM (fapeam.am.gov.br) e ler o edital do Programa de Apoio à Pesquisa em Empresas (PAPPE Integração).",
      "Cadastrar o proponente no sistema de submissão eletrônica SIGFAPEAM.",
      "Elaborar o projeto científico com orçamento detalhado voltado para a solução de gargalos do ecossistema local.",
      "Anexar a documentação de habilitação fiscal estadual e as certidões negativas.",
      "Submeter e aguardar a publicação dos resultados no Diário Oficial do Estado do Amazonas."
    ],
    suggested_projects: [
      "Desenvolvimento de plataformas web para logística inteligente e monitoramento na bacia amazônica.",
      "Desenvolvimento de biofármacos ou cosméticos inovadores a partir da flora amazônica."
    ]
  },
  "FAP PR": {
    name: "Fundação Araucária (FAP Paraná)",
    link: "https://www.fdr.pr.gov.br/Araucaria",
    description: "Fomento financeiro e bolsas estaduais para projetos de desenvolvimento e inovação no Paraná.",
    step_by_step: [
      "Acessar o portal da Fundação Araucária e verificar os editais abertos do Programa Prime ou de inovação empresarial.",
      "Cadastrar a empresa e a equipe de pesquisa na plataforma de submissão de projetos da fundação.",
      "Elaborar a proposta técnica focando na resolução de gargalos industriais ou agroindustriais do estado do Paraná.",
      "Montar o cronograma de faturamento, metas financeiras e contrapartida exigida de acordo com o porte da empresa.",
      "Submeter os documentos e acompanhar as avaliações do comitê paranaense."
    ],
    suggested_projects: [
      "Desenvolvimento de novos implementos agrícolas dotados de sensores inteligentes para o campo.",
      "Software de otimização de colheita integrado a dados de imagem de satélite."
    ]
  },
  "FAP SP": {
    name: "FAPESP (FAP São Paulo - Programa PIPE)",
    link: "https://fapesp.br/pipe",
    description: "Apoio financeiro de até R$ 1.5 milhão para projetos de P&D aplicados ao desenvolvimento comercial de novas tecnologias em SP.",
    step_by_step: [
      "Acessar o portal da FAPESP e ler as diretrizes do Programa PIPE (Pesquisa Inovativa em Pequenas Empresas - Fases 1, 2 e 3).",
      "Cadastrar os proponentes e o projeto na plataforma de submissão SAGe da FAPESP.",
      "Escrever a proposta de pesquisa inovadora demonstrando a viabilidade técnica comercial do projeto.",
      "Estruturar os gastos com consultorias de terceiros, bolsas para auxiliares de pesquisa e aquisição de equipamentos permanentes.",
      "Submeter a documentação e aguardar a análise de mérito científico pelos assessores de fomento."
    ],
    suggested_projects: [
      "Desenvolvimento de novos dispositivos médicos miniaturizados com sensores ópticos.",
      "Desenvolvimento de novas soluções biotecnológicas aplicadas ao refino de resíduos orgânicos."
    ]
  },
  "FAPs Estaduais": {
    name: "FAPs Estaduais (Fundações de Amparo à Pesquisa)",
    link: "https://www.confap.org.br",
    description: "Subvenções financeiras e fomento tecnológico administrados por fundações de amparo à pesquisa de cada estado brasileiro.",
    step_by_step: [
      "Identificar la FAP (Fundação de Amparo à Pesquisa) correspondente ao estado de registro da empresa.",
      "Acessar o portal da fundação estadual e ler os editais voltados a micro e pequenas empresas (Editais Tecnova/PAPPE).",
      "Cadastrar os pesquisadores no sistema local de submissão de projetos.",
      "Montar o plano de negócios e de pesquisa com metas de viabilidade econômica regional.",
      "Submeter o edital juntamente com as certidões fiscais de regularidade de FGTS, trabalhista e tributos estaduais/federais."
    ],
    suggested_projects: [
      "Pesquisa aplicada para aumento de eficiência energética em processos industriais locais.",
      "Desenvolvimento de novas interfaces ou aplicativos móveis para inclusão produtiva regional."
    ]
  },
  // Reduções Tributárias
  "Credito de ICMS sobre Insumos": {
    name: "Crédito de ICMS sobre Insumos Produtivos",
    link: "https://www.confaz.fazenda.gov.br",
    description: "Recuperação do ICMS pago na compra de matérias-primas e embalagens destinadas à industrialização de mercadorias.",
    step_by_step: [
      "Mapear todas as aquisições de insumos diretos, matérias-primas e embalagens que entram no processo de fabricação industrial.",
      "Verificar a alíquota de ICMS destacada nas notas fiscais de compra recebidas.",
      "Efetuar o cálculo mensal de créditos com base nas regras de crédito físico do Regulamento de ICMS (RICMS) estadual.",
      "Lançar os saldos credores apropriados na GIA/SPED Fiscal (EFD ICMS/IPI).",
      "Compensar o débito gerado nas saídas tributadas ou solicitar a transferência de saldos acumulados de acordo com a legislação do estado."
    ],
    suggested_projects: [
      "Projeto de auditoria fiscal e rastreamento de notas fiscais eletrônicas de entrada com inconsistência de ICMS destacado.",
      "Implementação de software ERP com módulo integrado de cálculo automático de crédito presumido estadual."
    ]
  },
  "Recuperacao de TUST/TUSD (Energia)": {
    name: "Exclusão da TUST/TUSD da Base de ICMS de Energia",
    link: "https://www.confaz.fazenda.gov.br",
    description: "Exclusão das tarifas de distribuição de energia elétrica da base de incidência do ICMS, permitindo recuperação histórica relevante.",
    step_by_step: [
      "Reunir as faturas mensais de energia elétrica consumida pela empresa dos últimos 60 meses.",
      "Identificar os valores cobrados sob as rubricas TUST (Tarifa de Uso do Sistema de Transmissão) e TUSD (Tarifa de Uso do Sistema de Distribuição).",
      "Efetuar o cálculo das diferenças apuradas excluindo a TUST e TUSD da base de incidência do ICMS destacado nas faturas.",
      "Ajuizar medida judicial apropriada para pleitear o direito de não recolher o imposto sobre essas tarifas de transmissão.",
      "Obter a sentença definitiva favorável e proceder à compensação administrativa via e-CAC ou SEFAZ estadual."
    ],
    suggested_projects: [
      "Auditoria de contas de energia integrada a plataforma IoT de controle de eficiência energética e demanda de ponta.",
      "Reestruturação de infraestrutura elétrica e instalação de subestação interna para se enquadrar no mercado livre de energia."
    ]
  },
  "Deducoes e Creditos do Agronegocio": {
    name: "Créditos Presumidos e Deduções do Agronegócio",
    link: "https://www.gov.br/receitafederal/pt-br",
    description: "Benefício fiscal concedido à cadeia agroindustrial para aliviar o custo tributário do produtor e da indústria alimentícia.",
    step_by_step: [
      "Identificar a elegibilidade para créditos presumidos de PIS e COFINS concedidos à agroindústria na aquisição de insumos agropecuários de pessoas físicas.",
      "Mapear as operações de compra de sementes, rações, adubos e animais de criadores diretos.",
      "Aplicar os coeficientes legais de crédito presumido (que variam de 35% a 60% da alíquota padrão) sobre os insumos agrícolas.",
      "Informar os valores de créditos acumulados na EFD Contribuições e compensá-los com outros tributos federais ou solicitar ressarcimento.",
      "Garantir a conformidade fiscal das autodeclarações perante a fiscalização do Ministério da Agricultura e Receita Federal."
    ],
    suggested_projects: [
      "Auditoria digital em notas fiscais do produtor (NFP-e) para regularização de cadastros rurais e aproveitamento de PIS/COFINS.",
      "Projetos de rastreamento de cadeia produtiva do agro com blockchain para certificar elegibilidade a incentivos de exportação."
    ]
  },
  "Creditos de PIS/COFINS Monofasico": {
    name: "Segregação de Receita de PIS/COFINS Monofásico",
    link: "https://www.gov.br/receitafederal/pt-br",
    description: "Restituição automática de impostos pagos indevidamente por comércios varejistas de produtos com tributação monofásica concentrada no fabricante.",
    step_by_step: [
      "Exportar todos os arquivos XML de notas fiscais de venda emitidas nos últimos 5 anos.",
      "Auditar os códigos NCM (Nomenclatura Comum do Mercosul) e CST de PIS/COFINS das notas fiscais das vendas realizadas.",
      "Isolar os produtos sujeitos ao regime de tributação monofásica (autopeças, perfumaria, medicamentos, bebidas).",
      "Retificar as declarações fiscais do Simples Nacional (PGDAS-D) ou EFD Contribuições deduzindo as receitas monofásicas da tributação de PIS/COFINS.",
      "Submeter o pedido eletrônico de restituição administrativa no portal do Simples Nacional ou e-CAC, obtendo o crédito em conta."
    ],
    suggested_projects: [
      "Auditoria retrospectiva de NCMs de estoque com correção e saneamento de cadastro tributário de produtos.",
      "Implantação de scanner fiscal automatizado no ponto de venda (PDV) para emissão correta de cupons fiscais."
    ]
  },
  // Inovações
  "Software": {
    name: "Incentivo ao Desenvolvimento de Software Nacional",
    link: "https://www.finep.gov.br",
    description: "Linhas de fomento e deduções para desenvolvimento, comercialização e registro de produtos digitais nacionais.",
    step_by_step: [
      "Comprovar que o software ou sistema desenvolvido possui propriedade intelectual registrada no INPI (Instituto Nacional de Propriedade Industrial).",
      "Identificar linhas de fomento exclusivas para o setor de TI (como editais Softex ou FINEP Inovação).",
      "Inscrever o produto no cadastro do BNDES Finame para permitir que clientes comprem a licença do software utilizando linhas de crédito subsidiadas.",
      "Manter a equipe técnica de programadores regularmente sob regime CLT para enquadrar as despesas de folha como custos dedutíveis de P&D.",
      "Documentar as sprints e metodologias ágeis utilizadas para comprovar a atividade de inovação do produto software."
    ],
    suggested_projects: [
      "Projetos de software para segurança de dados (LGPD) ou criptografia integrada.",
      "Desenvolvimento de plataformas proprietárias de ERP setorial ou SaaS voltadas à inteligência logística."
    ]
  },
  "Pesquisa & Desenvolvimento": {
    name: "Parcerias Acadêmicas de Pesquisa & Desenvolvimento (P&D)",
    link: "https://www.gov.br/mcti/pt-br",
    description: "Incentivos fiscais para fomento à inovação de produtos e processos cooperativos entre a iniciativa privada e universidades.",
    step_by_step: [
      "Estruturar os desafios e metas científicas que a empresa precisa superar em seu modelo de negócios.",
      "Identificar universidades federais ou estaduais que possuam laboratórios credenciados pelo CNPq/MCTI no segmento correspondente.",
      "Elaborar o acordo de cooperação técnica e de partilha de propriedade intelectual (PI) com o núcleo de inovação tecnológica (NIT) da universidade.",
      "Deduzir os aportes financeiros do imposto de renda da empresa e financiar bolsas de mestrado ou doutorado aplicadas.",
      "Monitorar o progresso científico por meio de relatórios conjuntos homologados pela universidade."
    ],
    suggested_projects: [
      "Pesquisa aplicada com laboratório de robótica para simulação e modelagem matemática de estresse de materiais.",
      "Projetos de biotecnologia agrícola em cooperação com laboratórios estaduais."
    ]
  },
  "Industria 4.0 & Automacao": {
    name: "Incentivo à Indústria 4.0 e Automação",
    link: "https://www.cni.com.br",
    description: "Programas de fomento e linhas de financiamento subsidiadas para modernização digital de plantas fabris.",
    step_by_step: [
      "Acessar o programa nacional 'Brasil Mais Produtivo' administrado pelo SENAI, ABDI e BNDES.",
      "Solicitar o diagnóstico industrial gratuito realizado pelos consultores credenciados do SENAI.",
      "Elaborar o plano de automação integrando sensores digitais, robótica cooperativa e computação na nuvem na planta fabril.",
      "Habilitar linhas de crédito pré-aprovadas com taxas de juros reduzidas (BNDES Finame Inovação) para aquisição de máquinas modernas.",
      "Monitorar o aumento de produtividade e redução de refugo e consumo elétrico."
    ],
    suggested_projects: [
      "Projetos de sensores inteligentes em esteiras transportadoras para manutenção preditiva em tempo real.",
      "Instalação de controladores lógicos programáveis (CLP) conectados a banco de dados em nuvem."
    ]
  },
  "Transformacao Digital": {
    name: "Incentivos de Fomento à Transformação Digital",
    link: "https://www.bndes.gov.br",
    description: "Financiamento facilitado para investimento em infraestrutura tecnológica, canais digitais de venda e computação empresarial.",
    step_by_step: [
      "Pesquisar programas ativos do BNDES voltados à modernização de pequenas e médias empresas (como BNDES Crédito Digital).",
      "Acessar a instituição bancária repassadora de sua preferência (ex: cooperativas de crédito ou bancos de desenvolvimento regional).",
      "Solicitar o enquadramento na linha de crédito para digitalização de canais de venda e compra de servidores/computadores.",
      "Apresentar a estimativa de impacto em vendas digitais, segurança cibernética e integração logística das novas ferramentas.",
      "Comprovar a compra e aplicação dos ativos digitais dentro das condições de juros reduzidos regulamentadas pela linha."
    ],
    suggested_projects: [
      "Migração de toda a infraestrutura física de servidores legados para servidores em nuvem resilientes.",
      "Criação e lançamento de plataformas digitais integradas (Omnichannel) e canais de e-commerce."
    ]
  }
};

// Estimativa de taxa tributária por CNAE
const getCnaeTaxRate = (code: string) => {
  if (code.startsWith("62") || code.startsWith("63") || code.startsWith("72")) {
    return "16.33% (ISS 5% + PIS/COFINS 9.25% + CPP)";
  }
  if (code.startsWith("45") || code.startsWith("47")) {
    return "11.18% (ICMS-ST + PIS/COFINS Monofásico)";
  }
  if (code.startsWith("10") || code.startsWith("20") || code.startsWith("28")) {
    return "14.25% (IPI médio + ICMS + PIS/COFINS)";
  }
  return "12.50% (Alíquota Média Geral)";
};

export default function Dashboard() {
  const [status, setStatus] = useState<string>("Aguardando conexão...");
  const [loading, setLoading] = useState(false);
  const [cnpj, setCnpj] = useState("");
  const [result, setResult] = useState<any>(null);
  
  // Controle de diagnóstico e animações
  const [showDiagnostics, setShowDiagnostics] = useState(false);
  const [diagnosticsLoading, setDiagnosticsLoading] = useState(false);
  const [balloons, setBalloons] = useState<any[]>([]);
  const [activeTab, setActiveTab] = useState<string>("opportunities");
  const [selectedItem, setSelectedItem] = useState<any>(null);

  // Controle de checklist e simulacao de RPA de certidoes
  const [checklistStates, setChecklistStates] = useState<Record<string, boolean[]>>({});
  const [rpaRunning, setRpaRunning] = useState<boolean>(false);
  const [rpaProgress, setRpaProgress] = useState<number>(0);
  const [rpaLogs, setRpaLogs] = useState<string[]>([]);
  const [emittedCertificates, setEmittedCertificates] = useState<Record<string, boolean>>({});

  // Calculadora interativa do Fator R
  const [fatorRFolha, setFatorRFolha] = useState<string>("");
  const [fatorRReceita, setFatorRReceita] = useState<string>("");
  const [selectedFatorRSector, setSelectedFatorRSector] = useState<string | null>(null);

  const FATOR_R_SECTORS = [
    { name: "Tecnologia & TI", folha: "35.000,00", receita: "100.000,00" },
    { name: "Marketing Consultivo", folha: "15.000,00", receita: "80.000,00" },
    { name: "Engenharia & Arquitetura", folha: "40.000,00", receita: "120.000,00" },
    { name: "Produção Intelectual", folha: "8.000,00", receita: "50.000,00" },
    { name: "Saúde Intelectualizada", folha: "30.000,00", receita: "90.000,00" },
    { name: "Serviços Técnicos", folha: "12.000,00", receita: "60.000,00" },
    { name: "Representação Comercial", folha: "20.000,00", receita: "70.000,00" },
    { name: "Academias & Atividades", folha: "25.000,00", receita: "80.000,00" }
  ];

  const selectSector = (sectorName: string) => {
    const sec = FATOR_R_SECTORS.find(s => s.name === sectorName);
    if (sec) {
      setSelectedFatorRSector(sectorName);
      setFatorRFolha(sec.folha);
      setFatorRReceita(sec.receita);
    }
  };

  const parseBRL = (v: string) => parseFloat(v.replace(/\./g, "").replace(",", ".")) || 0;
  const formatBRL = (v: string) => {
    const num = v.replace(/\D/g, "");
    if (!num) return "";
    return (parseInt(num) / 100).toLocaleString("pt-BR", { minimumFractionDigits: 2 });
  };
  const handleFolhaChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const raw = e.target.value.replace(/\D/g, "");
    setFatorRFolha(raw ? (parseInt(raw) / 100).toLocaleString("pt-BR", { minimumFractionDigits: 2 }) : "");
    setSelectedFatorRSector(null);
  };
  const handleReceitaChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const raw = e.target.value.replace(/\D/g, "");
    setFatorRReceita(raw ? (parseInt(raw) / 100).toLocaleString("pt-BR", { minimumFractionDigits: 2 }) : "");
    setSelectedFatorRSector(null);
  };

  // Upload de SPED para Módulo 6
  const [spedUploading, setSpedUploading] = useState<boolean>(false);
  const [spedFileUploaded, setSpedFileUploaded] = useState<string | null>(null);
  const [spedAuditResult, setSpedAuditResult] = useState<any>(null);

  const handleSpedUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    setSpedUploading(true);
    setSpedFileUploaded(file.name);
    setSpedAuditResult(null);
    
    const formData = new FormData();
    formData.append("cnpj", result?.cnpj || "");
    formData.append("file", file);
    
    try {
      const response = await fetch("/api/cnpj/upload-sped", {
        method: "POST",
        body: formData
      });
      if (response.ok) {
        const updatedResult = await response.json();
        setResult(updatedResult);
        setSpedAuditResult({
          status: "success",
          message: `Arquivo ${file.name} processado e integrado com sucesso!`,
          timestamp: new Date().toLocaleTimeString("pt-BR")
        });
      } else {
        const errorData = await response.json();
        setSpedAuditResult({
          status: "error",
          message: `Erro ao processar arquivo SPED: ${errorData.detail || "Erro no servidor"}`
        });
      }
    } catch (err: any) {
      setSpedAuditResult({
        status: "error",
        message: `Erro de rede/conexão: ${err.message || "Erro desconhecido"}`
      });
    } finally {
      setSpedUploading(false);
    }
  };

  const runRpaSimulation = (itemKey: string) => {
    setRpaRunning(true);
    setRpaProgress(0);
    setRpaLogs(["[00:00] Inicializando robo de consulta cadastral..."]);
    const logs = [
      "[00:01] Conectando ao e-CAC da Receita Federal com Certificado Digital A1...",
      "[00:03] Autenticado. Varrendo pendencias fiscais da Uniao...",
      "[00:05] Gerando Certidao Federal Conjunta PGFN/RFB...",
      "[00:07] Conectando a Caixa Economica Federal (CRF/FGTS)...",
      "[00:09] Emitindo Certificado de Regularidade do FGTS (CRF)...",
      "[00:11] Conectando ao Banco Nacional de Mandados de Prisao (BNMP/CNJ)...",
      "[00:13] Varredura BNMP concluida: nenhum mandado ativo encontrado.",
      "[00:15] Consultando Antecedentes Criminais na Policia Federal...",
      "[00:17] Certidao de Antecedentes da PF emitida com sucesso.",
      "[00:20] Integracao concluida! Certidoes prontas para download."
    ];
    let step = 0;
    const iv = setInterval(() => {
      step++;
      if (step < logs.length) {
        setRpaProgress(Math.floor((step / logs.length) * 100));
        setRpaLogs(prev => [...prev, logs[step]]);
      } else {
        clearInterval(iv);
        setRpaRunning(false);
        setRpaProgress(100);
        setEmittedCertificates(prev => ({ ...prev, [itemKey]: true }));
      }
    }, 1000);
  };

  const checkAPI = async () => {
    try {
      const res = await fetch("http://localhost:8003/health");
      const data = await res.json();
      setStatus(`Conectado: ${data.system} (v${data.version}) - Status: ${data.status}`);
    } catch (err) {
      setStatus("Falha de conexão com a API LexGrid. Verifique os contêineres.");
    }
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!cnpj) return;
    setLoading(true);
    setResult(null);
    setShowDiagnostics(false);
    try {
      const cleanedCnpj = cnpj.replace(/\D/g, "");
      const res = await fetch(`http://localhost:8003/api/v1/cnpj/${cleanedCnpj}`);
      if (res.ok) {
        let data = await res.json();
        
        // Storyboard Override: garante dados exatos do storyboard
        if (cleanedCnpj === "29093966000100") {
          data = {
            ...data,
            company_name: "Instituto Centro de Pesquisa e Desenvolvimento em Tecnologia de Software",
            trade_name: "ICP&D SOFTWARE",
            city: "MANAUS",
            state: "AM",
            company_size: "DEMAIS",
            capital_social: 2500000.00, // Capital Social real do Storyboard
            qsa: [
              {
                nome_socio: "AILTON FIGUEIRA DE QUEIROZ",
                qualificacao_socio: "Presidente",
                contato_email: "presidencia@empresa-demo.com.br",
                contato_telefone: "(92) 3216-9900"
              },
              {
                nome_socio: "ALESSANDRA DUARTE SILVA",
                qualificacao_socio: "Diretora Executiva",
                contato_email: "alessandra.duarte@empresa-demo.com.br",
                contato_telefone: "(92) 3216-9901"
              }
            ],
            potential_opportunities: ["lei_do_bem", "tust_tusd", "limitacao_base_terceiros_sistema_s"],
            divida_ativa_uniao: [
              {
                inscricao: "10178492023-99",
                valor: 145200.50,
                situacao: "Em cobrança ativa",
                tipo_devedor: "Principal",
                natureza: "Tributária"
              }
            ],
            fomentos_nao_reembolsaveis: [
              { orgao: "FINEP", tipo: "Subvenção Econômica", status: "Elegível (P&D)", descricao: "Recursos não reembolsáveis para projetos inovadores de risco tecnológico." },
              { orgao: "EMBRAPII", tipo: "Co-financiamento", status: "Elegível (Industrial/TI)", descricao: "Financiamento de até 1/3 do valor total do projeto de inovação em parceria com polos tecnológicos." },
              { orgao: "MCTI", tipo: "Editais Temáticos", status: "Elegível", descricao: "Programas nacionais de fomento à inteligência artificial corporativa." },
              { orgao: "CNPq", tipo: "Bolsas de Fomento", status: "Elegível", descricao: "Bolsas de fixação de pesquisadores em projetos de desenvolvimento." },
              { orgao: "CAPDA", tipo: "Fomento Tecnológico", status: "Elegível (Informática)", descricao: "Recursos de P&D geridos pelo Comitê das Atividades de Pesquisa e Desenvolvimento na Amazônia." },
              { orgao: "SUFRAMA", tipo: "Incentivo Regional", status: "Elegível (Zona Franca de Manaus)", descricao: "Isenção/redução tributária de IPI, PIS/COFINS de entrada para a região." }
            ],
            regime_simulacao: {
              faturamento_estimado: 50000000.0,
              criterio_porte: "DEMAIS",
              criterio_capital: 2500000.0,
              regimes: {
                simples_nacional: { elegivel: false, aliquota_media: "N/A", custo_estimado: 0, vantagem: "Inelegível devido ao limite de faturamento anual (> R$ 4.8M)." },
                lucro_presumido: { elegivel: true, aliquota_media: "16.33%", custo_estimado: 8165000, vantagem: "Adequado para margens de lucro elevadas, mas impede uso da Lei do Bem." },
                lucro_real: { elegivel: true, aliquota_media: "34.0% (IRPJ/CSLL) + 9.25% (PIS/COFINS)", custo_estimado: 6450000, vantagem: "Recomendado. Permite dedução integral da Lei do Bem e créditos de P&D." }
              },
              recomendacao: "Lucro Real",
              detalhe_recomendacao: "Recomendação baseada na alta elegibilidade para a Lei do Bem e incentivos do CAPDA/SUFRAMA."
            },
            reducao_tributaria: [
              { oportunidade: "Recuperação de TUST/TUSD (Energia)", origem: "Judicial/Estadual", descricao: "Exclusão das tarifas de distribuição e transmissão de energia da base de cálculo do ICMS." },
              { oportunidade: "Dedução e Crédito de ICMS - Lei de Informática", origem: "Estadual", descricao: "Crédito presumido de ICMS para bens eletrônicos e de informática produzidos de acordo com o PPB." }
            ],
            reforma_tributaria: {
              impacto_geral: "Favorável com Atenções",
              aliquota_estimada_ibs_cbs: "26.5% (Teto do Governo)",
              pontos_positivos: [
                "Fim do efeito cascata com crédito físico e financeiro amplo.",
                "Simplificação drástica das obrigações acessórias.",
                "Manutenção integral dos incentivos federais da Lei do Bem."
              ],
              pontos_negativos: [
                "Alíquota nominal de serviços (IBS/CBS) deve subir, exigindo gestão eficiente de créditos.",
                "Complexidade no período híbrido de transição (2026-2033)."
              ],
              imposto_seletivo: "Inaplicável"
            },
            incentivos_inovacao: [
              { tipo: "Software", incentivo: "Financiamentos FINEP Inovação e Credenciamento no BNDES Finame para comercialização de licenças de software nacional." },
              { tipo: "Pesquisa & Desenvolvimento", incentivo: "Parcerias universidade-empresa sob o marco legal da ciência e tecnologia com dedução fiscal." },
              { tipo: "Transformação Digital", incentivo: "Crédito para digitalização industrial e investimento em infraestrutura de TI." }
            ],
            fontes_consultadas: [
              { fonte: "Receita Federal", nivel: 1, status: "Consultado - OK", tipo: "Dados Cadastrais e Situação Fiscal" },
              { fonte: "CONFAZ", nivel: 1, status: "Conectado", tipo: "Convênios de ICMS e Benefícios Estaduais" },
              { fonte: "FINEP", nivel: 1, status: "Sincronizado", tipo: "Programas de Subvenção de Inovação" },
              { fonte: "BNDES", nivel: 1, status: "Conectado", tipo: "Linhas de Crédito e Fomentos Ativos" },
              { fonte: "EMBRAPII", nivel: 1, status: "Sincronizado", tipo: "Unidades Credenciadas e Parcerias" },
              { fonte: "ANEEL", nivel: 1, status: "Não Aplicável", tipo: "Incentivos P&D Setor Elétrico" },
              { fonte: "SUFRAMA", nivel: 1, status: "Sincronizado", tipo: "Incentivos Regionais ZFM" },
              { fonte: "CAPDA", nivel: 1, status: "Conectado", tipo: "Atividades de P&D de TI na Amazônia" },
              { fonte: "Editais Estaduais (FAPs)", nivel: 2, status: "Varredura Concluída", tipo: "Editais e Subvenções Locais" },
              { fonte: "Diários Oficiais da União e Estados", nivel: 2, status: "Monitoramento Ativo", tipo: "Leis e Portarias de Incentivo" },
              { fonte: "Portais Governamentais Estaduais", nivel: 2, status: "Varredura Concluída", tipo: "Regulamentos ICMS Estaduais" }
            ],
            score_global: 56,
            nivel_alerta: "Atenção",
            scores_dimensionais: { financeiro: 38, compliance: 58, operacional: 82, mercado: 70 },
            swot: {
              forcas: [
                "Capital social de R$ 2,5M e estrutura financeira solidária e ativa.",
                "CNPJ ativo há mais de 10 anos com histórico contínuo de regularidade.",
                "Máxima elegibilidade para Lei do Bem (Lucro Real + P&D intensivo).",
                "Operações na Zona Franca de Manaus com incentivos SUFRAMA/CAPDA garantidos.",
                "Equipe técnica especializada em software — Goodwill e propriedade intelectual elevados."
              ],
              fraquezas: [
                "Inadimplência formalizada identificada (Títulos Protestados ativos). Risco de bloqueio de crédito na praça.",
                "Dívida ativa inscrita na PGFN de R$ 145.200,50 — exige regularização prioritária.",
                "Score de compliance tributário 58/100 — risco latente de malha fina fiscal.",
                "Exposição a autoções por não aproveitamento histórico de créditos de TUST/TUSD.",
                "Pendência federal bloqueia emissão de CND e participação em editais públicos."
              ],
              oportunidades: [
                "Recuperação estimada de R$ 600k a R$ 1,8M via Lei do Bem nos últimos 5 anos.",
                "Subvenção econômica FINEP Inovação — edital aberto com prazo até 12/2025.",
                "Co-financiamento EMBRAPII de até 1/3 do projeto de TI sem necessidade de reembolso.",
                "Reforma Tributária (IBS/CBS) mantém 100% dos incentivos da Lei do Bem intactos.",
                "FAPEAM (FAP Amazonas) com edital PAPPE aberto para MPEs do setor de TI."
              ],
              ameacas: [
                "Aliquota efetiva de serviços no novo IBS/CBS estimada em 26,5% — alta para TI.",
                "Período de transição híbrido 2026-2033 exige dupla conformidade fiscal simultânea.",
                "Inadimplência tributaria pode restringir acesso a licitações e contratos públicos.",
                "Inflação de custos de mão-de-obra TI pressiona margens — monitoramento SIDRA/IBGE."
              ]
            },
            parecer_executivo: "### PARECER EXECUTIVO DE ANÁLISE DE RISCOS E MITIGAÇÃO\n\n**Diagnóstico de Risco Geral:** A empresa está classificada sob o status de **ATENÇÃO (Risco Moderado)** com pontuação ponderada de **56/100**.\n\nA empresa encontra-se em um patamar de risco moderado. A principal vulnerabilidade financeira é a presença de dois títulos protestados ativos em cartórios, além da dívida ativa de R$ 145.200,50 inscrita na PGFN, comprometendo o score financeiro (38/100).\n\n**Plano de Mitigação Sugerido:**\n1. **Regularização de Crédito**: Providenciar a quitação imediata dos títulos junto ao credor e solicitar a baixa do protesto no cartório emissor, ou obter certidão positiva com efeito de negativa para resguardar o rating de crédito.\n2. **Regularização Fiscal**: Efetuar a renegociação ou adesão aos programas de transação tributária da PGFN para regularizar os débitos ativos e obter a CND.\n3. **Proteção de Caixa**: Iniciar o aproveitamento dos incentivos fiscais da Lei do Bem (potencial de R$ 780.000,00/ano não aproveitado) para gerar fôlego financeiro.",
            protestos: [
              {
                cartorio: "1º Cartório de Protesto de Letras e Títulos - Manaus/AM",
                documento_protestado: "Duplicata de Prestação de Serviços",
                valor: 12500.00,
                data_protesto: "2025-11-10",
                status: "ATIVO",
                anuencia_solicitada: false
              },
              {
                cartorio: "2º Cartório de Protesto de Letras e Títulos - Manaus/AM",
                documento_protestado: "Nota Promissória",
                valor: 8400.00,
                data_protesto: "2026-02-18",
                status: "ATIVO",
                anuencia_solicitada: true
              }
            ],
            cyber_intel: {
              cyber_score: 38,
              nivel: "Crítico",
              attack_surface: {
                portas_expostas: [
                  { porta: 3389, servico: "RDP (Remote Desktop Protocol)", risco: "CRÍTICO", ip: "177.84.112.43", cve: "CVE-2019-0708 (BlueKeep)" },
                  { porta: 22,   servico: "SSH OpenSSH 7.4",              risco: "ALTO",    ip: "177.84.112.43", cve: "CVE-2018-15919" },
                  { porta: 9200, servico: "Elasticsearch 7.x (sem auth)", risco: "CRÍTICO", ip: "177.84.112.44", cve: "Exposição de dados sem autenticação" },
                  { porta: 443,  servico: "HTTPS/443",                    risco: "OK",      ip: "177.84.112.43", cve: "" }
                ],
                ssl_valido: true,
                ssl_expira_em: "45 dias",
                tecnologias_legadas: ["Apache/2.2.31 — CVE-2017-9798 (RottenTomato)", "PHP/5.6.40 — End of Life"]
              },
              dark_web: {
                credenciais_vazadas: 3,
                emails_comprometidos: ["financeiro@empresa-demo.com.br", "ti@empresa-demo.com.br"],
                data_ultimo_vazamento: "Nov/2024",
                breaches: [
                  { fonte: "RockYou2024",    data: "Jun/2024", severidade: "CRÍTICO", tipo: "Senha em Texto Claro", emails: 2 },
                  { fonte: "Collection #1",  data: "Jan/2019", severidade: "ALTO",    tipo: "Hash MD5 Quebrável",   emails: 1 },
                  { fonte: "LinkedIn 2012",  data: "Jun/2012", severidade: "MÉDIO",   tipo: "Hash SHA-1",           emails: 1 }
                ]
              },
              osint_findings: [
                { tipo: "PDF Indexado",      nome: "proposta-comercial-q3-2024.pdf",  severidade: "ALTO",    url: "https://empresa-demo.com.br/docs/proposta-q3-2024.pdf" },
                { tipo: "Config Exposta",    nome: ".env backup no repositório GitHub público", severidade: "CRÍTICO", url: "https://github.com/empresa-demo/api-config" },
                { tipo: "Planilha Indexada", nome: "orcamento-folha-2024.xlsx",       severidade: "ALTO",    url: "https://empresa-demo.com.br/rh/orcamento-2024.xlsx" }
              ],
              recomendacoes: [
                { prioridade: "URGENTE", acao: "Fechar porta RDP 3389 à internet e exigir VPN corporativa para acesso remoto." },
                { prioridade: "URGENTE", acao: "Elasticsearch 9200 exposto sem autenticação — habilitar X-Pack Security imediatamente." },
                { prioridade: "URGENTE", acao: "Resetar credenciais de financeiro@ e ti@ e habilitar MFA (autentificador TOTP)." },
                { prioridade: "URGENTE", acao: "Remover arquivo .env do repositório GitHub e revogar todas as chaves de API expostas." },
                { prioridade: "ALTO",    acao: "Renovar certificado SSL — expira em 45 dias (risco de downtime e phishing)." },
                { prioridade: "ALTO",    acao: "Atualizar Apache para versão atual e migrar PHP 5.6 para PHP 8.x (EOL)." },
                { prioridade: "MÉDIO",   acao: "Solicitar remoção do PDF indexado via Google Search Console." }
              ]
            }
          };
        }
        
        setResult(data);
      } else {
        const errData = await res.json();
        setResult({ error: errData.detail || "CNPJ não encontrado ou erro na API." });
      }
    } catch (err) {
      setResult({ error: "Falha ao conectar com o motor de enriquecimento do LexGrid." });
    } finally {
      setLoading(false);
    }
  };

  // Dispara a animação de balões caindo do topo
  const triggerBalloons = () => {
    const colors = ["#f43f5e", "#0ea5e9", "#eab308", "#22c55e", "#ec4899", "#a855f7"];
    const newBalloons = Array.from({ length: 45 }).map((_, i) => ({
      id: i,
      left: `${Math.random() * 100}%`,
      color: colors[Math.floor(Math.random() * colors.length)],
      delay: `${Math.random() * 2.0}s`,
      duration: `${3.5 + Math.random() * 2}s`,
      size: `${22 + Math.random() * 22}px`
    }));
    setBalloons(newBalloons);
    setTimeout(() => setBalloons([]), 7000);
  };

  // Ação de Gerar Diagnóstico
  const handleGenerateDiagnostics = () => {
    setDiagnosticsLoading(true);
    setTimeout(() => {
      setDiagnosticsLoading(false);
      setShowDiagnostics(true);
      triggerBalloons();
      setActiveTab("roadmap");
    }, 1200);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-sky-500 selection:text-slate-950 relative overflow-x-hidden">
      
      {/* CSS Keyframes para Animação de Balões */}
      <style dangerouslySetInnerHTML={{__html: `
        @keyframes balloonFall {
          0% {
            transform: translateY(-100px) rotate(0deg);
            opacity: 1;
          }
          90% {
            opacity: 1;
          }
          100% {
            transform: translateY(115vh) rotate(360deg);
            opacity: 0;
          }
        }
        .falling-balloon {
          position: fixed;
          top: -80px;
          border-radius: 50% 50% 50% 50% / 40% 40% 60% 60%;
          animation: balloonFall 5s linear forwards;
          z-index: 10000;
          pointer-events: none;
        }
        .falling-balloon::after {
          content: "";
          position: absolute;
          bottom: -8px;
          left: 45%;
          border-left: 4px solid transparent;
          border-right: 4px solid transparent;
          border-bottom: 8px solid currentColor;
        }
      `}} />

      {/* Renderização Dinâmica dos Balões */}
      {balloons.map((b) => (
        <div 
          key={b.id}
          className="falling-balloon"
          style={{
            left: b.left,
            backgroundColor: b.color,
            color: b.color,
            width: b.size,
            height: `calc(${b.size} * 1.3)`,
            animationDelay: b.delay,
            animationDuration: b.duration
          }}
        />
      ))}

      {/* Ambient background glow */}
      <div className="absolute top-0 left-0 w-full h-[500px] bg-gradient-to-b from-sky-950/20 via-transparent to-transparent pointer-events-none" />
      
      <div className="p-4 md:p-8 max-w-7xl mx-auto space-y-8 relative z-10">
        
        {/* Navigation & Header */}
        <header className="flex flex-col md:flex-row md:items-center md:justify-between border-b border-slate-800/80 pb-6 gap-4">
          <div className="space-y-1">
            <h1 className="text-3xl md:text-4xl font-extrabold flex items-center gap-3 tracking-tight bg-gradient-to-r from-sky-400 to-indigo-400 bg-clip-text text-transparent">
              <ShieldAlert className="text-sky-400 w-9 h-9" />
              LexGrid <span className="text-slate-500 font-medium text-lg md:text-xl tracking-normal">| Corporate AI</span>
            </h1>
            <p className="text-slate-400 text-sm md:text-base">Diagnóstico de Segurança e Oportunidades Tributárias Corporativas</p>
          </div>
          
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 bg-slate-900/60 p-3 rounded-xl border border-slate-800 backdrop-blur-sm">
            <div className="flex items-center gap-2">
              <Activity className="text-sky-400 w-5 h-5 shrink-0 animate-pulse" />
              <span className="text-xs font-mono text-slate-300 max-w-[200px] truncate">{status}</span>
            </div>
            <button 
              onClick={checkAPI} 
              className="text-xs bg-slate-800 hover:bg-slate-700 active:bg-slate-800 text-slate-200 px-3 py-1.5 rounded-lg border border-slate-700 transition-colors font-medium"
            >
              Testar Conexão API
            </button>
          </div>
        </header>

        {/* 1. Busca por Empresa (Identificação e Varredura) */}
        <section className="bg-slate-900/85 border border-slate-800/80 p-6 md:p-8 rounded-2xl shadow-xl backdrop-blur-sm space-y-4">
          <div className="space-y-1">
            <h2 className="text-lg font-bold flex items-center gap-2 text-sky-300">
              <Search size={18} className="text-sky-400" />
              Identificação e Varredura
            </h2>
            <p className="text-slate-400 text-xs md:text-sm">Digite o CNPJ abaixo para varrer as bases governamentais e identificar o enquadramento fiscal.</p>
          </div>
          
          <form onSubmit={handleSearch} className="flex flex-col sm:flex-row gap-4">
            <input 
              type="text" 
              placeholder="Digite o CNPJ (somente números)..." 
              value={cnpj}
              onChange={(e) => setCnpj(e.target.value)}
              className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-slate-100 placeholder-slate-600 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500/20 transition-all font-mono text-sm md:text-base"
              disabled={loading}
            />
            <button 
              type="submit" 
              className="bg-sky-500 hover:bg-sky-400 active:bg-sky-500 text-slate-950 font-bold px-8 py-3 rounded-xl transition-all shadow-lg shadow-sky-500/10 flex items-center justify-center gap-2 disabled:opacity-50 text-sm md:text-base shrink-0"
              disabled={loading}
            >
              {loading ? (
                <>
                  <svg className="animate-spin h-5 w-5 text-slate-950" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Buscando...
                </>
              ) : (
                <>
                  Analisar CNPJ
                  <ArrowRight size={18} />
                </>
              )}
            </button>
          </form>
        </section>

        {/* 2. Exibição de Dados (Result Card & Company Details) */}
        {result && (
          <div className="space-y-8 animate-fadeIn">
            
            {result.error ? (
              <div className="bg-red-500/10 border border-red-500/20 p-5 rounded-2xl flex items-center gap-3 text-red-400">
                <AlertTriangle className="shrink-0" />
                <span className="font-semibold text-sm">{result.error}</span>
              </div>
            ) : (
              <>
                {/* Identification Card */}
                <div className="bg-gradient-to-br from-slate-900 to-slate-950 border border-slate-800 p-6 md:p-8 rounded-2xl shadow-lg relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-32 h-32 bg-sky-500/5 rounded-full blur-3xl pointer-events-none" />
                  
                  <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
                    <div className="space-y-2">
                      <div className="flex items-center gap-3 flex-wrap">
                        <span className="text-xs font-mono font-bold px-2.5 py-1 bg-slate-800 text-slate-300 rounded-lg border border-slate-700">
                          CNPJ: {result.cnpj.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/, "$1.$2.$3/$4-$5")}
                        </span>
                        <span className="px-3 py-1 text-xs font-bold rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase tracking-wide">
                          ATIVA | {result.city} ({result.state})
                        </span>
                      </div>
                      
                      <h2 className="text-2xl md:text-3xl font-extrabold text-white leading-tight">
                        {result.company_name}
                      </h2>
                      {result.trade_name && (
                        <p className="text-slate-400 text-sm">
                          Nome Fantasia: <span className="text-slate-300">{result.trade_name}</span>
                        </p>
                      )}
                    </div>
                    
                    <div className="bg-slate-900 border border-slate-800/80 p-4 rounded-xl flex flex-col items-start gap-1 font-mono shrink-0">
                      <span className="text-[10px] text-slate-500 uppercase font-bold">Capital Social</span>
                      <span className="text-emerald-400 font-extrabold text-lg">
                        {new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(result.capital_social || 0.0)}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Sub-details: QSA (President Contact) & CNAEs (with tax rates) */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                  
                  {/* Left block (2/3 width): CNAEs & Tax Rates */}
                  <div className="lg:col-span-2 bg-slate-900/60 border border-slate-800/80 p-6 rounded-2xl space-y-4 backdrop-blur-sm shadow-md">
                    <h3 className="text-md font-bold text-sky-300 flex items-center gap-2 uppercase tracking-wide text-xs border-b border-slate-800 pb-2">
                      <Building2 size={16} />
                      CNAEs Secundários e Taxas de Tributação
                    </h3>
                    
                    <div className="space-y-3">
                      {/* Main CNAE */}
                      <div className="bg-slate-950 p-4 rounded-xl border border-slate-800/60 flex items-start justify-between gap-4">
                        <div className="space-y-1">
                          <span className="text-[10px] text-slate-500 uppercase font-bold">CNAE Principal</span>
                          <p className="text-slate-200 text-sm font-semibold leading-normal">
                            <span className="font-mono text-sky-400 mr-2">{result.main_cnae.codigo}</span>
                            {result.main_cnae.descricao}
                          </p>
                        </div>
                        <div className="text-right shrink-0">
                          <span className="text-[10px] text-slate-500 uppercase font-bold block font-sans">Taxa Estimada</span>
                          <span className="text-xs font-mono font-bold bg-sky-950 text-sky-400 px-2 py-1 rounded border border-sky-900/40">
                            {getCnaeTaxRate(result.main_cnae.codigo)}
                          </span>
                        </div>
                      </div>

                      {/* Secondary CNAEs with specific rates */}
                      <div className="space-y-2.5">
                        <span className="text-[10px] text-slate-500 uppercase font-bold block">Atividades Secundárias</span>
                        {result.secondary_cnaes && result.secondary_cnaes.length > 0 ? (
                          <div className="grid grid-cols-1 gap-2.5 max-h-48 overflow-y-auto pr-1">
                            {result.secondary_cnaes.map((cnae: any, idx: number) => (
                              <div key={idx} className="bg-slate-950/40 p-3.5 rounded-lg border border-slate-900/60 flex items-center justify-between gap-4">
                                <div className="min-w-0 flex-1">
                                  <p className="text-slate-300 text-xs font-medium leading-normal truncate">
                                    <span className="font-mono text-slate-400 mr-2">{cnae.codigo}</span>
                                    {cnae.descricao}
                                  </p>
                                </div>
                                <div className="text-right shrink-0 font-mono text-[11px] font-bold text-slate-400 bg-slate-900 px-2 py-0.5 rounded">
                                  {getCnaeTaxRate(cnae.codigo)}
                                </div>
                              </div>
                            ))}
                          </div>
                        ) : (
                          <p className="text-xs text-slate-600 italic">Nenhum CNAE secundário vinculado.</p>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Right block (1/3 width): Contact info for President (QSA) */}
                  <div className="bg-slate-900/60 border border-slate-800/80 p-6 rounded-2xl space-y-4 backdrop-blur-sm shadow-md flex flex-col justify-between">
                    <div className="space-y-4">
                      <h3 className="text-md font-bold text-sky-300 flex items-center gap-2 uppercase tracking-wide text-xs border-b border-slate-800 pb-2">
                        <Users size={16} />
                        Direção Executiva e Contatos (QSA)
                      </h3>

                      {result.qsa && result.qsa.length > 0 ? (
                        <div className="space-y-4">
                          {result.qsa.map((partner: any, idx: number) => {
                            const isPresident = partner.qualificacao_socio?.toLowerCase().includes("presidente") || idx === 0;
                            return (
                              <div key={idx} className={`p-4 rounded-xl border ${isPresident ? "bg-sky-950/20 border-sky-900/35" : "bg-slate-950 border-slate-900"} space-y-2`}>
                                <div className="flex items-center gap-2">
                                  <Briefcase size={14} className="text-sky-400" />
                                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                                    {partner.qualificacao_socio || "Diretor"}
                                  </span>
                                </div>
                                <div className="text-xs font-bold text-white uppercase">{partner.nome_socio || partner.nome}</div>
                                
                                {/* President Specific contacts */}
                                <div className="space-y-1 pt-1 text-[11px] text-slate-400 border-t border-slate-800/40">
                                  <div className="flex items-center gap-1.5 font-mono">
                                    <Mail size={12} className="text-slate-500" />
                                    <span className="truncate">{partner.contato_email || "presidencia@empresa-demo.com.br"}</span>
                                  </div>
                                  <div className="flex items-center gap-1.5 font-mono">
                                    <Phone size={12} className="text-slate-500" />
                                    <span>{partner.contato_telefone || "(92) 3216-9900"}</span>
                                  </div>
                                </div>
                              </div>
                            );
                          })}
                        </div>
                      ) : (
                        <p className="text-xs text-slate-600 italic">Quadro societário simplificado indisponível.</p>
                      )}
                    </div>
                  </div>
                </div>

                {/* Direct Opportunities Display (Showing Return Value and Tax Reform Impact immediately!) */}
                <section className="space-y-6">
                  <div className="border-l-4 border-sky-400 pl-3">
                    <h3 className="text-xl font-extrabold tracking-tight text-white flex items-center gap-2">
                      <DollarSign className="text-sky-400" />
                      Mapeamento de Oportunidades Fiscais Identificadas
                    </h3>
                    <p className="text-slate-400 text-xs md:text-sm mt-0.5">
                      Veja a estimativa de retorno e o impacto da reforma tributária (IBS/CBS) identificados especificamente para o CNPJ desta empresa.
                    </p>
                  </div>

                  {result.potential_opportunities && result.potential_opportunities.length > 0 ? (
                    <div className="grid grid-cols-1 gap-6">
                      {result.potential_opportunities.map((oppId: string, idx: number) => {
                        const opp = getOpportunityDetail(oppId);
                        const IconComponent = opp.icon;
                        
                        return (
                          <div key={idx} className="bg-slate-900 border border-slate-800/80 rounded-2xl shadow-lg overflow-hidden hover:border-slate-700/60 transition-colors">
                            
                            {/* Card Header (Title & Return Potential) */}
                            <div className="bg-slate-950/70 p-5 border-b border-slate-800/80 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                              <div className="flex items-center gap-3">
                                <div className="w-9 h-9 rounded-lg bg-sky-950/50 border border-sky-900/40 flex items-center justify-center shrink-0">
                                  <IconComponent className="text-sky-400 w-5 h-5" />
                                </div>
                                <div>
                                  <h4 className="text-base font-extrabold text-white leading-normal">{opp.name}</h4>
                                  <span className="text-[10px] font-mono font-bold text-slate-500">ID: {oppId}</span>
                                </div>
                              </div>
                              <div className="flex items-center gap-2 bg-sky-950/40 px-3 py-1.5 rounded-lg border border-sky-900/30 text-sky-400">
                                <DollarSign size={16} />
                                <span className="text-xs font-extrabold font-mono tracking-wide">{opp.estimated_potential}</span>
                              </div>
                            </div>

                            {/* Card Body (Two Columns: Legal & Action / Tax Reform Impact) */}
                            <div className="p-6 grid grid-cols-1 lg:grid-cols-2 gap-6 bg-slate-900/40">
                              {/* Left Column: Legal Grounding */}
                              <div className="space-y-2">
                                <div className="text-xs font-bold text-slate-400 flex items-center gap-1.5">
                                  <BookOpen size={14} className="text-sky-400" />
                                  Embasamento Jurídico e Regulatório
                                </div>
                                <p className="text-xs md:text-sm text-slate-300 leading-relaxed font-semibold">{opp.base_legal}</p>
                                <p className="text-xs text-slate-400 leading-relaxed">Este direito protege e viabiliza a conformidade fiscal das operações da empresa, com base em entendimentos consolidados nos Tribunais Superiores (STF/STJ).</p>
                              </div>

                              {/* Right Column: Tax Reform Impact (IBS/CBS) */}
                              <div className="bg-slate-950 p-4 rounded-xl border border-slate-850/80 space-y-2 self-start">
                                <div className="text-xs font-bold text-amber-400 flex items-center gap-1.5">
                                  <Scale size={14} />
                                  Impacto na Nova Reforma Tributária (IBS/CBS)
                                </div>
                                <p className="text-xs text-slate-400 leading-relaxed font-medium">{opp.tax_reform}</p>
                              </div>
                            </div>
                            
                          </div>
                        );
                      })}
                    </div>
                  ) : (
                    <div className="bg-slate-900 border border-slate-800 p-8 rounded-2xl text-center">
                      <HelpCircle className="mx-auto w-12 h-12 text-slate-600 mb-2" />
                      <p className="text-slate-400 text-sm font-medium">Nenhuma oportunidade mapeada de forma direta para esta empresa.</p>
                    </div>
                  )}
                </section>

                {/* 3. Geração de Diagnóstico (The Large Red Action Button) */}
                <div className="text-center py-6 border-t border-b border-slate-850/80">
                  {!showDiagnostics ? (
                    <button
                      onClick={handleGenerateDiagnostics}
                      className="bg-red-600 hover:bg-red-500 active:bg-red-600 text-white font-extrabold px-12 py-5 rounded-2xl transition-all shadow-xl shadow-red-600/20 hover:scale-105 active:scale-100 flex items-center justify-center gap-3 mx-auto text-base md:text-lg tracking-wide uppercase"
                      disabled={diagnosticsLoading}
                    >
                      {diagnosticsLoading ? (
                        <>
                          <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          Processando Auditoria...
                        </>
                      ) : (
                        <>
                          Gerar Diagnóstico de Recuperação Fiscal
                          <ArrowDown size={20} className="animate-bounce" />
                        </>
                      )}
                    </button>
                  ) : (
                    <div className="bg-emerald-500/10 border border-emerald-500/20 p-4 rounded-xl max-w-md mx-auto text-emerald-400 text-sm font-semibold flex items-center justify-center gap-2">
                      <CheckCircle2 size={18} />
                      Diagnóstico de Recuperação Fiscal Gerado com Sucesso!
                    </div>
                  )}
                </div>

                {/* 4. Navegação nos Resultados (Executive Roadmap tabs unlocked post-animation) */}
                {showDiagnostics && (
                  <section className="space-y-6 animate-fadeIn">
                    
                    {/* Navigation Tabs Header */}
                    <div className="flex border-b border-slate-800 overflow-x-auto gap-2 p-1 bg-slate-900/60 rounded-xl border border-slate-800 backdrop-blur-sm">
                      <button
                        onClick={() => setActiveTab("opportunities")}
                        className={`px-5 py-3 rounded-lg text-xs md:text-sm font-bold tracking-wide transition-all shrink-0 uppercase ${
                          activeTab === "opportunities"
                            ? "bg-sky-500 text-slate-950 shadow-md font-extrabold"
                            : "text-slate-400 hover:text-slate-200 hover:bg-slate-800"
                        }`}
                      >
                        Oportunidades & Fomentos
                      </button>
                      <button
                        onClick={() => setActiveTab("simulador")}
                        className={`px-5 py-3 rounded-lg text-xs md:text-sm font-bold tracking-wide transition-all shrink-0 uppercase ${
                          activeTab === "simulador"
                            ? "bg-sky-500 text-slate-950 shadow-md font-extrabold"
                            : "text-slate-400 hover:text-slate-200 hover:bg-slate-800"
                        }`}
                      >
                        Simulador Tributário
                      </button>
                      <button
                        onClick={() => setActiveTab("score")}
                        className={`px-5 py-3 rounded-lg text-xs md:text-sm font-bold tracking-wide transition-all shrink-0 uppercase ${
                          activeTab === "score"
                            ? "bg-rose-500 text-white shadow-md font-extrabold"
                            : "text-slate-400 hover:text-slate-200 hover:bg-slate-800"
                        }`}
                      >
                        Score &amp; SWOT
                      </button>
                      <button
                        onClick={() => setActiveTab("reforma")}
                        className={`px-5 py-3 rounded-lg text-xs md:text-sm font-bold tracking-wide transition-all shrink-0 uppercase ${
                          activeTab === "reforma"
                            ? "bg-sky-500 text-slate-950 shadow-md font-extrabold"
                            : "text-slate-400 hover:text-slate-200 hover:bg-slate-800"
                        }`}
                      >
                        Reforma Tributária
                      </button>
                      <button
                        onClick={() => setActiveTab("incentives")}
                        className={`px-5 py-3 rounded-lg text-xs md:text-sm font-bold tracking-wide transition-all shrink-0 uppercase ${
                          activeTab === "incentives"
                            ? "bg-emerald-600 text-white shadow-md font-extrabold"
                            : "text-slate-400 hover:text-slate-200 hover:bg-slate-800"
                        }`}
                      >
                        Incentivos &amp; Crédito
                      </button>
                      <button
                        onClick={() => setActiveTab("cyber")}
                        className={`px-5 py-3 rounded-lg text-xs md:text-sm font-bold tracking-wide transition-all shrink-0 uppercase ${
                          activeTab === "cyber"
                            ? "bg-rose-600 text-white shadow-md font-extrabold"
                            : "text-slate-400 hover:text-slate-200 hover:bg-slate-800"
                        }`}
                      >
                        Cyber Intel
                      </button>
                      <button
                        onClick={() => setActiveTab("compliance")}
                        className={`px-5 py-3 rounded-lg text-xs md:text-sm font-bold tracking-wide transition-all shrink-0 uppercase ${
                          activeTab === "compliance"
                            ? "bg-sky-500 text-slate-950 shadow-md font-extrabold"
                            : "text-slate-400 hover:text-slate-200 hover:bg-slate-800"
                        }`}
                      >
                        Compliance, Riscos & Fontes
                      </button>
                    </div>

                    {/* Tabs Content */}
                    <div className="bg-slate-900 border border-slate-800 p-6 md:p-8 rounded-2xl shadow-xl space-y-6">
                      
                      {/* TAB 1: Oportunidades & Fomentos */}
                      {activeTab === "opportunities" && (
                        <div className="space-y-8">
                          
                          {/* 1.1 Fomentos Não Reembolsáveis */}
                          <div className="space-y-4">
                            <div className="border-l-4 border-sky-400 pl-3">
                              <h4 className="text-lg font-bold text-white">Fomentos Não Reembolsáveis Mapeados</h4>
                              <p className="text-slate-400 text-xs mt-0.5">Recursos financeiros públicos para incentivo que não precisam ser devolvidos. Clique no card para ver o passo a passo de como obter o edital.</p>
                            </div>
                            
                            {result.fomentos_nao_reembolsaveis && result.fomentos_nao_reembolsaveis.length > 0 ? (
                              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {result.fomentos_nao_reembolsaveis.map((f: any, idx: number) => (
                                  <div 
                                    key={idx} 
                                    onClick={() => setSelectedItem({ ...f, key: f.orgao })}
                                    className="cursor-pointer hover:scale-[1.01] active:scale-[0.99] transition-all bg-slate-950/60 border border-slate-850 p-4 rounded-xl space-y-2 hover:border-sky-500/40 hover:bg-slate-950"
                                  >
                                    <div className="flex items-center justify-between">
                                      <span className="text-xs font-mono font-extrabold text-sky-400 uppercase bg-sky-950/30 px-2 py-0.5 rounded border border-sky-900/20">{f.orgao}</span>
                                      <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">{f.status}</span>
                                    </div>
                                    <div className="text-xs font-bold text-white">{f.tipo}</div>
                                    <p className="text-xs text-slate-400 leading-relaxed">{f.descricao}</p>
                                    <div className="text-[10px] text-sky-400 font-bold flex items-center gap-1 pt-1">
                                      <span>Ver passo a passo do Edital</span>
                                      <ArrowRight size={10} />
                                    </div>
                                  </div>
                                ))}
                              </div>
                            ) : (
                              <p className="text-xs text-slate-500 italic">Nenhum fomento não reembolsável direto mapeado para o perfil.</p>
                            )}
                          </div>

                          {/* 1.2 Incentivos Fiscais & Plano de Ação */}
                          <div className="space-y-4">
                            <div className="border-l-4 border-sky-400 pl-3">
                              <h4 className="text-lg font-bold text-white">Planos de Ação para Incentivos Fiscais</h4>
                              <p className="text-slate-400 text-xs mt-0.5">Planejamento e ações estruturadas para recuperação de benefícios fiscais. Clique para ver o enquadramento de projetos.</p>
                            </div>

                            {result.potential_opportunities && result.potential_opportunities.length > 0 ? (
                              <div className="space-y-4">
                                {result.potential_opportunities.map((oppId: string, idx: number) => {
                                  const opp = getOpportunityDetail(oppId);
                                  return (
                                    <div 
                                      key={idx} 
                                      onClick={() => setSelectedItem({ ...opp, key: oppId, is_opp: true })}
                                      className="cursor-pointer hover:border-sky-500/40 transition-all bg-slate-950/40 p-5 rounded-xl border border-slate-850 space-y-3 hover:bg-slate-950/60"
                                    >
                                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-900 pb-2">
                                        <h5 className="text-sm font-extrabold text-white uppercase flex items-center gap-2">
                                          <CheckCircle2 size={16} className="text-sky-400" />
                                          Plano de Ação: {opp.name}
                                        </h5>
                                        <span className="text-[10px] font-mono text-amber-400 font-bold bg-amber-500/5 px-2 py-0.5 rounded border border-amber-500/10">Incentivo Fiscal / Clique para ver Projetos</span>
                                      </div>
                                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                        {opp.action_plan.map((step: string, sIdx: number) => (
                                          <div key={sIdx} className="bg-slate-950 border border-slate-900 p-3 rounded-lg flex items-start gap-2.5">
                                            <span className="w-5 h-5 rounded-full bg-sky-950 text-sky-400 text-[10px] font-bold flex items-center justify-center shrink-0 border border-sky-900/30">
                                              {sIdx + 1}
                                            </span>
                                            <p className="text-xs text-slate-400 leading-relaxed font-medium">{step}</p>
                                          </div>
                                        ))}
                                      </div>
                                    </div>
                                  );
                                })}
                              </div>
                            ) : (
                              <p className="text-xs text-slate-500 italic">Nenhum plano de ação de incentivo fiscal mapeado.</p>
                            )}
                          </div>

                          {/* 1.3 Reduções Tributárias & Incentivos de Inovação */}
                          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                            {/* Redução Tributária */}
                            <div className="space-y-4 bg-slate-950 p-5 rounded-xl border border-slate-900">
                              <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider border-b border-slate-900 pb-2 flex items-center gap-1.5">
                                <DollarSign size={14} className="text-sky-400" />
                                Oportunidades de Redução Tributária
                              </h5>
                              <div className="space-y-3">
                                {result.reducao_tributaria && result.reducao_tributaria.length > 0 ? (
                                  result.reducao_tributaria.map((r: any, idx: number) => (
                                    <div 
                                      key={idx} 
                                      onClick={() => setSelectedItem({ name: r.oportunidade, description: r.descricao, key: r.oportunidade })}
                                      className="cursor-pointer hover:border-sky-500/40 p-3 rounded-lg border border-slate-900/60 flex items-center justify-between gap-4 hover:bg-slate-950 transition-all"
                                    >
                                      <div className="space-y-1">
                                        <span className="text-xs font-bold text-white">{r.oportunidade}</span>
                                        <p className="text-[11px] text-slate-400 leading-relaxed">{r.descricao}</p>
                                      </div>
                                      <span className="text-[9px] font-mono font-bold bg-slate-900 px-2 py-0.5 rounded text-slate-400 border border-slate-800 shrink-0">{r.origem}</span>
                                    </div>
                                  ))
                                ) : (
                                  <p className="text-xs text-slate-650 italic">Nenhuma redução tributária geral mapeada.</p>
                                )}
                              </div>
                            </div>

                            {/* Incentivos de Inovação */}
                            <div className="space-y-4 bg-slate-950 p-5 rounded-xl border border-slate-900">
                              <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider border-b border-slate-900 pb-2 flex items-center gap-1.5">
                                <Brain size={14} className="text-sky-400" />
                                Incentivos de Inovação (Setorial)
                              </h5>
                              <div className="space-y-3">
                                {result.incentivos_inovacao && result.incentivos_inovacao.length > 0 ? (
                                  result.incentivos_inovacao.map((i: any, idx: number) => (
                                    <div 
                                      key={idx} 
                                      onClick={() => setSelectedItem({ name: i.tipo, description: i.incentivo, key: i.tipo })}
                                      className="cursor-pointer hover:border-sky-500/40 p-3 rounded-lg border border-slate-900/60 hover:bg-slate-950 transition-all"
                                    >
                                      <span className="text-xs font-bold text-sky-300 block">{i.tipo}</span>
                                      <p className="text-[11px] text-slate-400 leading-relaxed">{i.incentivo}</p>
                                    </div>
                                  ))
                                ) : (
                                  <p className="text-xs text-slate-650 italic">Nenhum incentivo de inovação mapeado.</p>
                                )}
                              </div>
                            </div>
                          </div>

                        </div>
                      )}

                      {/* TAB 2: Simulador Tributário & Regimes */}
                      {activeTab === "simulador" && result.regime_simulacao && (
                        <div className="space-y-6">
                          <div className="border-l-4 border-sky-400 pl-3">
                            <h4 className="text-lg font-bold text-white">Simulador Comparativo de Regimes Tributários</h4>
                            <p className="text-slate-400 text-xs mt-0.5">Diagnóstico contábil completo de carga fiscal anual para enquadramento ideal.</p>
                          </div>

                          {/* Recommendation card */}
                          <div className="bg-gradient-to-r from-sky-950/30 to-slate-950 border border-sky-900/30 p-5 rounded-2xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                            <div className="space-y-1">
                              <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider block">Regime Recomendado pela IA</span>
                              <div className="flex items-center gap-2">
                                <span className="text-lg font-extrabold text-sky-400 uppercase tracking-wide bg-sky-950/50 px-3 py-1 rounded-xl border border-sky-900/30">
                                  {result.regime_simulacao.recomendacao}
                                </span>
                                <span className="text-xs text-emerald-400 font-bold flex items-center gap-1">
                                  <CheckCircle2 size={12} />
                                  Cenário de Maior Economia
                                </span>
                              </div>
                              <p className="text-xs text-slate-400 pt-1 max-w-xl font-medium">{result.regime_simulacao.detalhe_recomendacao}</p>
                            </div>

                            <div className="flex gap-4 border-l border-slate-800 pl-0 md:pl-6 shrink-0 font-mono text-xs text-slate-400">
                              <div className="space-y-0.5">
                                <span className="text-[9px] text-slate-500 block uppercase font-bold">Faturamento Estimado</span>
                                <span className="font-bold text-slate-200">
                                  {new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(result.regime_simulacao.faturamento_estimado || 0)}
                                </span>
                              </div>
                              <div className="space-y-0.5">
                                <span className="text-[9px] text-slate-500 block uppercase font-bold">Porte Validador</span>
                                <span className="font-bold text-slate-200">{result.regime_simulacao.criterio_porte}</span>
                              </div>
                            </div>
                          </div>

                          {/* Comparison Grid Table (Efetiva e comparativa) */}
                          <div className="bg-slate-950 p-4 rounded-xl border border-slate-900 overflow-x-auto">
                            <table className="w-full text-left text-xs border-collapse min-w-[600px]">
                              <thead>
                                <tr className="border-b border-slate-800 text-slate-500 font-bold uppercase text-[10px]">
                                  <th className="pb-3 text-left">Regime Tributário</th>
                                  <th className="pb-3">Elegibilidade</th>
                                  <th className="pb-3 text-right">Alíquota Efetiva Média</th>
                                  <th className="pb-3 text-right">Custo Tributário Anual</th>
                                  <th className="pb-3 text-right">Economia Anual Projetada</th>
                                </tr>
                              </thead>
                              <tbody>
                                {/* Simples Nacional */}
                                <tr className={`border-b border-slate-900/50 ${result.regime_simulacao.recomendacao === "Simples Nacional" ? "bg-sky-950/10" : ""}`}>
                                  <td className="py-3.5 font-bold text-white">Simples Nacional</td>
                                  <td>
                                    <span className={`text-[9px] font-bold px-2 py-0.5 rounded ${result.regime_simulacao.regimes.simples_nacional.elegivel ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20" : "bg-red-500/10 text-red-400 border border-red-500/20"}`}>
                                      {result.regime_simulacao.regimes.simples_nacional.elegivel ? "ELEGÍVEL" : "INELEGÍVEL"}
                                    </span>
                                  </td>
                                  <td className="text-right font-mono font-bold text-slate-300">
                                    {result.regime_simulacao.regimes.simples_nacional.aliquota_media}
                                  </td>
                                  <td className="text-right font-mono font-bold text-white">
                                    {result.regime_simulacao.regimes.simples_nacional.elegivel 
                                      ? new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(result.regime_simulacao.regimes.simples_nacional.custo_estimado)
                                      : "R$ 0,00"}
                                  </td>
                                  <td className="text-right text-slate-500 font-mono font-semibold">
                                    -
                                  </td>
                                </tr>

                                {/* Lucro Presumido */}
                                <tr className={`border-b border-slate-900/50 ${result.regime_simulacao.recomendacao === "Lucro Presumido" ? "bg-sky-950/10" : ""}`}>
                                  <td className="py-3.5 font-bold text-white">Lucro Presumido</td>
                                  <td>
                                    <span className="text-[9px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">ELEGÍVEL</span>
                                  </td>
                                  <td className="text-right font-mono font-bold text-slate-300">
                                    {result.regime_simulacao.regimes.lucro_presumido.aliquota_media}
                                  </td>
                                  <td className="text-right font-mono font-bold text-white">
                                    {new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(result.regime_simulacao.regimes.lucro_presumido.custo_estimado)}
                                  </td>
                                  <td className="text-right text-slate-500 font-mono font-semibold">
                                    {result.regime_simulacao.recomendacao === "Lucro Presumido" ? (
                                      <span className="text-emerald-400 font-bold">
                                        Economia de {new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(Math.max(0, result.regime_simulacao.regimes.lucro_real.custo_estimado - result.regime_simulacao.regimes.lucro_presumido.custo_estimado))}
                                      </span>
                                    ) : "Referência (Base)"}
                                  </td>
                                </tr>

                                {/* Lucro Real */}
                                <tr className={`border-b border-slate-900/50 ${result.regime_simulacao.recomendacao === "Lucro Real" ? "bg-sky-950/20 border border-sky-900/30" : ""}`}>
                                  <td className="py-3.5 font-bold text-white flex items-center gap-1">
                                    Lucro Real
                                    <span className="text-[8px] font-extrabold bg-sky-500 text-slate-950 px-1 py-0.2 rounded font-sans uppercase">Ideal</span>
                                  </td>
                                  <td>
                                    <span className="text-[9px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">ELEGÍVEL</span>
                                  </td>
                                  <td className="text-right font-mono font-bold text-sky-400">
                                    {result.regime_simulacao.regimes.lucro_real.aliquota_media}
                                  </td>
                                  <td className="text-right font-mono font-extrabold text-sky-400">
                                    {new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(result.regime_simulacao.regimes.lucro_real.custo_estimado)}
                                  </td>
                                  <td className="text-right font-mono font-bold">
                                    {result.regime_simulacao.recomendacao === "Lucro Real" ? (
                                      <span className="text-emerald-400 font-extrabold">
                                        Economia de {new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(Math.max(0, result.regime_simulacao.regimes.lucro_presumido.custo_estimado - result.regime_simulacao.regimes.lucro_real.custo_estimado))}
                                      </span>
                                    ) : "Referência (Base)"}
                                  </td>
                                </tr>
                              </tbody>
                            </table>
                          </div>

                          {/* O que foi verificado na Simulação? */}
                          <div className="bg-slate-950 p-5 rounded-xl border border-slate-900 space-y-3">
                            <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Metodologia e Critérios de Governança Fiscal Validados</h5>
                            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs font-medium pt-1 text-slate-300">
                              <div className="bg-slate-900 p-3 rounded border border-slate-850">
                                <span className="text-[10px] text-slate-500 block font-bold">Volume de Faturamento</span>
                                Avaliação de limites de sublimite estadual do Simples (R$ 3.6M) e teto de enquadramento (R$ 4.8M / R$ 78M).
                              </div>
                              <div className="bg-slate-900 p-3 rounded border border-slate-850">
                                <span className="text-[10px] text-slate-500 block font-bold">Verificação de CNAEs ({1 + (result.secondary_cnaes?.length || 0)} Validados)</span>
                                Rastreamento de atividades vedadas em 100% dos CNAEs secundários perante a LC 123/2006.
                              </div>
                              <div className="bg-slate-900 p-3 rounded border border-slate-850">
                                <span className="text-[10px] text-slate-500 block font-bold">Estrutura Societária (QSA)</span>
                                Análise de composição societária e verificação de participação em outras PJ do grupo econômico.
                              </div>
                              <div className="bg-slate-900 p-3 rounded border border-slate-850">
                                <span className="text-[10px] text-slate-500 block font-bold">Aproveitamento da Lei do Bem</span>
                                Elegibilidade técnica ao diferimento fiscal de despesas em inovação exclusivas de Lucro Real.
                              </div>
                            </div>
                          </div>

                          {/* Planejamento Tributário Imediato (Ações práticas para reduzir impostos hoje) */}
                          <div className="bg-slate-950 p-5 rounded-xl border border-slate-900 space-y-4">
                            <div className="border-b border-slate-900 pb-2">
                              <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                                <TrendingUp size={14} className="text-sky-400" />
                                Planejamento Tributário Imediato (Como Reduzir Impostos Hoje)
                              </h5>
                              <p className="text-slate-500 text-[10px] mt-0.5">Ações jurídicas e administrativas que podem ser adotadas imediatamente para diminuir a carga fiscal atual.</p>
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                              <div className="p-3.5 bg-slate-900 border border-slate-850 rounded-lg space-y-1 hover:border-slate-800 transition-colors">
                                <div className="flex items-center justify-between text-xs font-bold text-white">
                                  <span>1. Enquadramento e Uso da Lei do Bem</span>
                                  <span className="text-[8px] font-extrabold bg-sky-950 text-sky-400 px-1.5 py-0.2 rounded border border-sky-900/30">Federal</span>
                                </div>
                                <p className="text-[11px] text-slate-400 leading-relaxed">Estruture os projetos tecnológicos de desenvolvimento de software e deduza até 34% de IRPJ/CSLL dos custos de folha dos programadores sob Lucro Real.</p>
                              </div>

                              <div className="p-3.5 bg-slate-900 border border-slate-850 rounded-lg space-y-1 hover:border-slate-800 transition-colors">
                                <div className="flex items-center justify-between text-xs font-bold text-white">
                                  <span>2. Exclusão do ICMS na Base de PIS/COFINS</span>
                                  <span className="text-[8px] font-extrabold bg-sky-950 text-sky-400 px-1.5 py-0.2 rounded border border-sky-900/30">Judicial / Federal</span>
                                </div>
                                <p className="text-[11px] text-slate-400 leading-relaxed">Proponha retificação de obrigações acessórias (Tema 69 do STF) e reouve o imposto pago a maior nos últimos 5 anos, reduzindo faturas correntes.</p>
                              </div>

                              <div className="p-3.5 bg-slate-900 border border-slate-850 rounded-lg space-y-1 hover:border-slate-800 transition-colors">
                                <div className="flex items-center justify-between text-xs font-bold text-white">
                                  <span>3. Exclusão de TUST/TUSD da Fatura de Energia</span>
                                  <span className="text-[8px] font-extrabold bg-sky-950 text-sky-400 px-1.5 py-0.2 rounded border border-sky-900/30">Judicial / Estadual</span>
                                </div>
                                <p className="text-[11px] text-slate-400 leading-relaxed">Interponha medida jurídica para retirar as taxas de transmissão da base de cálculo do ICMS de energia, gerando economia contínua nas faturas fabris.</p>
                              </div>

                              <div className="p-3.5 bg-slate-900 border border-slate-850 rounded-lg space-y-1 hover:border-slate-800 transition-colors">
                                <div className="flex items-center justify-between text-xs font-bold text-white">
                                  <span>4. Segregação Contábil de Monofásicos</span>
                                  <span className="text-[8px] font-extrabold bg-sky-950 text-sky-400 px-1.5 py-0.2 rounded border border-sky-900/30">Administrativo</span>
                                </div>
                                <p className="text-[11px] text-slate-400 leading-relaxed">Saneie o cadastro de NCMs de produtos e retire os tributos de PIS/COFINS monofásicos da guia de recolhimento no PGDAS-D ou EFD.</p>
                              </div>
                            </div>
                          </div>

                        </div>
                      )}

                      {/* TAB SCORE: Score Global & Matriz SWOT */}
                      {activeTab === "score" && (() => {
                        const score = result.score_global ?? 72;
                        const nivel = result.nivel_alerta ?? "Saudável";
                        const dims = result.scores_dimensionais ?? { financeiro: 78, compliance: 58, operacional: 82, mercado: 70 };
                        const swot = result.swot ?? { forcas: [], fraquezas: [], oportunidades: [], ameacas: [] };
                        const parecer = result.parecer_executivo ?? "";
                        const scoreBg = score >= 70 ? "from-emerald-950/60 to-slate-950 border-emerald-900/40" : score >= 40 ? "from-amber-950/60 to-slate-950 border-amber-900/40" : "from-red-950/60 to-slate-950 border-red-900/40";
                        const scoreRing = score >= 70 ? "border-emerald-500 text-emerald-400" : score >= 40 ? "border-amber-500 text-amber-400" : "border-red-500 text-red-400";
                        const nivelColor = score >= 70 ? "text-emerald-400 bg-emerald-500/10 border-emerald-500/30" : score >= 40 ? "text-amber-400 bg-amber-500/10 border-amber-500/30" : "text-red-400 bg-red-500/10 border-red-500/30";
                        const dimColors: Record<string, string> = { financeiro: "bg-sky-500", compliance: "bg-amber-500", operacional: "bg-emerald-500", mercado: "bg-purple-500" };
                        const dimLabels: Record<string, string> = { financeiro: "Financeiro / Crédito (40%)", compliance: "Compliance / Tributário (30%)", operacional: "Operacional / Cibernético (15%)", mercado: "Mercado / Macroeconômico (15%)" };
                        return (
                          <div className="space-y-6">
                            <div className="border-l-4 border-rose-500 pl-3">
                              <h4 className="text-lg font-bold text-white">Score Global de Risco & Matriz SWOT Estratégica</h4>
                              <p className="text-slate-400 text-xs mt-0.5">Motor preditivo de análise corporativa baseado em 4 dimensões ponderadas (Financeiro 40% | Compliance 30% | Operacional 15% | Mercado 15%).</p>
                            </div>

                            {/* Score + Dimensoes */}
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                              {/* Score Gauge */}
                              <div className={`bg-gradient-to-br ${scoreBg} border p-6 rounded-2xl flex flex-col items-center justify-center text-center space-y-3 col-span-1`}>
                                <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Score Global</span>
                                <div className={`w-28 h-28 rounded-full border-[6px] flex flex-col items-center justify-center ${scoreRing}`}>
                                  <span className="text-4xl font-black">{score}</span>
                                  <span className="text-[9px] font-bold text-slate-500">/ 100</span>
                                </div>
                                <span className={`text-xs font-extrabold px-3 py-1 rounded-full border uppercase tracking-wider ${nivelColor}`}>{nivel}</span>
                                <div className="text-[10px] text-slate-500 leading-relaxed">
                                  <span className="text-red-400 font-bold">0-39</span> Crítico &nbsp;|&nbsp; <span className="text-amber-400 font-bold">40-69</span> Atenção &nbsp;|&nbsp; <span className="text-emerald-400 font-bold">70-100</span> Saudável
                                </div>
                              </div>

                              {/* Dimensional Scores */}
                              <div className="col-span-2 bg-slate-950 border border-slate-800 p-6 rounded-2xl space-y-4">
                                <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Scores Dimensionais — Pesos Calibrados</h5>
                                {(Object.entries(dims) as [string, number][]).map(([key, val]) => (
                                  <div key={key} className="space-y-1.5">
                                    <div className="flex items-center justify-between text-xs">
                                      <span className="font-semibold text-slate-300">{dimLabels[key] ?? key}</span>
                                      <span className={`font-extrabold font-mono ${val >= 70 ? "text-emerald-400" : val >= 40 ? "text-amber-400" : "text-red-400"}`}>{val}/100</span>
                                    </div>
                                    <div className="w-full h-2.5 bg-slate-900 rounded-full overflow-hidden">
                                      <div className={`h-full rounded-full transition-all ${dimColors[key] ?? "bg-sky-500"}`} style={{ width: `${val}%` }} />
                                    </div>
                                  </div>
                                ))}
                              </div>
                            </div>

                            {/* SWOT 2x2 */}
                            <div className="space-y-3">
                              <div className="flex items-center gap-2">
                                <div className="w-3 h-3 rounded-sm bg-rose-500" />
                                <h5 className="text-sm font-extrabold text-white uppercase tracking-wide">Análise Estratégica Corporativa</h5>
                              </div>
                              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                {/* Forcas */}
                                <div className="bg-emerald-950/20 border border-emerald-500/30 rounded-2xl overflow-hidden">
                                  <div className="bg-emerald-500/15 px-5 py-3 flex items-center gap-2 border-b border-emerald-500/20">
                                    <span className="w-6 h-6 rounded-md bg-emerald-500 flex items-center justify-center text-white text-[10px] font-black">S</span>
                                    <span className="font-extrabold text-emerald-400 text-xs uppercase tracking-widest">Forças (Strengths)</span>
                                  </div>
                                  <ul className="p-5 space-y-2">
                                    {swot.forcas?.map((f: string, i: number) => (
                                      <li key={i} className="flex items-start gap-2 text-xs text-slate-300 leading-relaxed">
                                        <span className="text-emerald-500 font-black mt-0.5 shrink-0">+</span>
                                        <span>{f}</span>
                                      </li>
                                    ))}
                                  </ul>
                                </div>
                                {/* Fraquezas */}
                                <div className="bg-red-950/20 border border-red-500/30 rounded-2xl overflow-hidden">
                                  <div className="bg-red-500/15 px-5 py-3 flex items-center gap-2 border-b border-red-500/20">
                                    <span className="w-6 h-6 rounded-md bg-red-500 flex items-center justify-center text-white text-[10px] font-black">W</span>
                                    <span className="font-extrabold text-red-400 text-xs uppercase tracking-widest">Fraquezas (Weaknesses)</span>
                                  </div>
                                  <ul className="p-5 space-y-2">
                                    {swot.fraquezas?.map((f: string, i: number) => (
                                      <li key={i} className="flex items-start gap-2 text-xs text-slate-300 leading-relaxed">
                                        <span className="text-red-500 font-black mt-0.5 shrink-0">!</span>
                                        <span>{f}</span>
                                      </li>
                                    ))}
                                  </ul>
                                </div>
                                {/* Oportunidades */}
                                <div className="bg-sky-950/20 border border-sky-500/30 rounded-2xl overflow-hidden">
                                  <div className="bg-sky-500/15 px-5 py-3 flex items-center gap-2 border-b border-sky-500/20">
                                    <span className="w-6 h-6 rounded-md bg-sky-500 flex items-center justify-center text-white text-[10px] font-black">O</span>
                                    <span className="font-extrabold text-sky-400 text-xs uppercase tracking-widest">Oportunidades (Opportunities)</span>
                                  </div>
                                  <ul className="p-5 space-y-2">
                                    {swot.oportunidades?.map((f: string, i: number) => (
                                      <li key={i} className="flex items-start gap-2 text-xs text-slate-300 leading-relaxed">
                                        <span className="text-sky-400 font-black mt-0.5 shrink-0">&#8593;</span>
                                        <span>{f}</span>
                                      </li>
                                    ))}
                                  </ul>
                                </div>
                                {/* Ameacas */}
                                <div className="bg-amber-950/20 border border-amber-500/30 rounded-2xl overflow-hidden">
                                  <div className="bg-amber-500/15 px-5 py-3 flex items-center gap-2 border-b border-amber-500/20">
                                    <span className="w-6 h-6 rounded-md bg-amber-500 flex items-center justify-center text-slate-950 text-[10px] font-black">T</span>
                                    <span className="font-extrabold text-amber-400 text-xs uppercase tracking-widest">Ameaças (Threats)</span>
                                  </div>
                                  <ul className="p-5 space-y-2">
                                    {swot.ameacas?.map((f: string, i: number) => (
                                      <li key={i} className="flex items-start gap-2 text-xs text-slate-300 leading-relaxed">
                                        <span className="text-amber-500 font-black mt-0.5 shrink-0">&#8595;</span>
                                        <span>{f}</span>
                                      </li>
                                    ))}
                                  </ul>
                                </div>
                              </div>
                            </div>

                            {/* Catalogo de Riscos Empresariais */}
                            <div className="space-y-3">
                              <h5 className="text-sm font-extrabold text-white uppercase tracking-wide flex items-center gap-2">
                                <span className="w-3 h-3 rounded-sm bg-rose-500" />
                                Catálogo de Riscos Empresariais
                              </h5>
                              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div className="bg-slate-950 border border-slate-800 rounded-2xl overflow-hidden">
                                  <div className="bg-orange-500/10 border-b border-orange-500/20 px-4 py-3 flex items-center gap-2">
                                    <span className="w-2 h-2 rounded-full bg-orange-500" />
                                    <span className="font-bold text-orange-400 text-xs uppercase tracking-widest">Riscos Financeiros</span>
                                    <span className="text-[9px] text-slate-500 ml-auto">Impacto direto no DRE e Fluxo de Caixa</span>
                                  </div>
                                  <div className="p-4 space-y-2">
                                    {[["Mercado","Variações de preços, câmbio, juros e inflação.","amber"],["Crédito","Clientes inadimplentes e concentração em poucos compradores.","red"],["Contraparte","Fornecedores estratégicos que falham na entrega crítica.","orange"],["Liquidez","Falta de caixa para honrar compromissos de curto prazo.","rose"],["Operacional","Falhas de processos, estoques mal geridos, paradas.","amber"],["Modelo de Negócio","Estratégias falhas ou dependência de um único produto.","slate"]].map(([label, desc, color]) => (
                                      <div key={label} className="flex items-start gap-3 p-2.5 rounded-lg hover:bg-slate-900 transition-colors">
                                        <div className={`w-2 h-2 rounded-full bg-${color}-500 mt-1 shrink-0`} />
                                        <div>
                                          <span className="text-xs font-bold text-white block">{label}</span>
                                          <span className="text-[11px] text-slate-500">{desc}</span>
                                        </div>
                                      </div>
                                    ))}
                                  </div>
                                </div>
                                <div className="bg-slate-950 border border-slate-800 rounded-2xl overflow-hidden">
                                  <div className="bg-indigo-500/10 border-b border-indigo-500/20 px-4 py-3 flex items-center gap-2">
                                    <span className="w-2 h-2 rounded-full bg-indigo-500" />
                                    <span className="font-bold text-indigo-400 text-xs uppercase tracking-widest">Riscos Não-Financeiros</span>
                                    <span className="text-[9px] text-slate-500 ml-auto">Impacto reputacional e de longo prazo</span>
                                  </div>
                                  <div className="p-4 space-y-2">
                                    {[["Compliance","Multas por descumprimento de normas fiscais, trabalhistas e ambientais.","red"],["Conduta","Fraudes internas, corrupção e desvios éticos.","rose"],["Reputacional","Perda de confiança de clientes e parceiros, crises de imagem.","purple"],["Investimento","Escolhas ruins em expansão, aquisições ou CAPEX sem retorno.","amber"],["Tributário","Passivos fiscais ocultos, autuções e malha fina recorrente.","orange"],["Cibernético","Portas expostas (Shodan), vazamentos de dados e ataques.","sky"]].map(([label, desc, color]) => (
                                      <div key={label} className="flex items-start gap-3 p-2.5 rounded-lg hover:bg-slate-900 transition-colors">
                                        <div className={`w-2 h-2 rounded-full bg-${color}-500 mt-1 shrink-0`} />
                                        <div>
                                          <span className="text-xs font-bold text-white block">{label}</span>
                                          <span className="text-[11px] text-slate-500">{desc}</span>
                                        </div>
                                      </div>
                                    ))}
                                  </div>
                                </div>
                              </div>
                            </div>

                            {/* Calculadora Interativa do Fator R */}
                             {(() => {
                               const folhaNum = parseBRL(fatorRFolha);
                               const receitaNum = parseBRL(fatorRReceita);
                               const fatorR = receitaNum > 0 ? (folhaNum / receitaNum) * 100 : null;
                               const migra = fatorR !== null && fatorR >= 28;
                               const aliqAtual = 15.5; const aliqOtim = 6.0;
                               const economiaAnual = receitaNum > 0 ? receitaNum * 12 * ((aliqAtual - aliqOtim) / 100) : 0;
                               const economiaReal = receitaNum > 0 && fatorR !== null ? receitaNum * 12 * ((aliqAtual - aliqOtim) / 100) : 0;
                               const isSimples = result.regime_simulacao?.regimes?.simples_nacional?.elegivel;
                               const fmtCurrency = (v: number) => v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
                               return (
                                 <div className="bg-slate-950 border border-slate-800 rounded-2xl overflow-hidden">
                                   <div className="bg-gradient-to-r from-sky-900/30 to-slate-950 px-5 py-4 border-b border-slate-800 flex items-center justify-between">
                                     <div>
                                       <h5 className="font-extrabold text-white text-sm">Calculadora do Fator R — Simples Nacional</h5>
                                       <p className="text-slate-400 text-xs mt-0.5">Preencha os valores abaixo. O sistema calcula automaticamente se sua empresa pode migrar do Anexo V (15,5%) para o Anexo III (6%).</p>
                                     </div>
                                     {fatorR !== null && (
                                       <div className={`shrink-0 px-3 py-1.5 rounded-xl border text-xs font-extrabold uppercase ${migra ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/30" : "bg-red-500/10 text-red-400 border-red-500/30"}`}>
                                         {migra ? "✓ Migra Anexo III" : "✗ Permanece Anexo V"}
                                       </div>
                                     )}
                                   </div>
                                   <div className="p-5 space-y-5">
                                     {/* Inputs */}
                                     <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                       <div className="space-y-1.5">
                                         <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
                                           Folha de Pagamentos — últimos 12 meses (R$)
                                         </label>
                                         <div className="relative">
                                           <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 text-sm font-bold">R$</span>
                                           <input
                                             type="text"
                                             inputMode="numeric"
                                             value={fatorRFolha}
                                             onChange={handleFolhaChange}
                                             placeholder="0,00"
                                             className="w-full bg-slate-900 border border-slate-700 rounded-xl pl-9 pr-4 py-3 text-white font-mono text-sm focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500/20 transition-all"
                                           />
                                         </div>
                                         <p className="text-[10px] text-slate-600">Salários + pró-labore + INSS patronal + FGTS</p>
                                       </div>
                                       <div className="space-y-1.5">
                                         <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
                                           Receita Bruta — últimos 12 meses (R$)
                                         </label>
                                         <div className="relative">
                                           <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 text-sm font-bold">R$</span>
                                           <input
                                             type="text"
                                             inputMode="numeric"
                                             value={fatorRReceita}
                                             onChange={handleReceitaChange}
                                             placeholder="0,00"
                                             className="w-full bg-slate-900 border border-slate-700 rounded-xl pl-9 pr-4 py-3 text-white font-mono text-sm focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500/20 transition-all"
                                           />
                                         </div>
                                         <p className="text-[10px] text-slate-600">Faturamento total dos últimos 12 meses</p>
                                       </div>
                                     </div>

                                     {/* Resultado */}
                                     {fatorR !== null ? (
                                       <div className={`rounded-2xl border overflow-hidden ${migra ? "border-emerald-500/30 bg-emerald-950/20" : "border-red-500/30 bg-red-950/20"}`}>
                                         <div className={`px-5 py-3 border-b flex items-center justify-between ${migra ? "border-emerald-500/20 bg-emerald-500/10" : "border-red-500/20 bg-red-500/10"}`}>
                                           <span className={`text-xs font-extrabold uppercase tracking-wider ${migra ? "text-emerald-400" : "text-red-400"}`}>
                                             {migra ? "✓ Fator R Atingido — Migração Recomendada!" : "✗ Fator R Abaixo do Limite — Estratégias Necessárias"}
                                           </span>
                                           <span className={`text-2xl font-black font-mono ${migra ? "text-emerald-400" : "text-red-400"}`}>
                                             {fatorR.toFixed(2).replace(".", ",")}%
                                           </span>
                                         </div>
                                         <div className="p-5 grid grid-cols-1 md:grid-cols-3 gap-4">
                                           <div className="text-center">
                                             <span className="text-[10px] text-slate-500 uppercase font-bold block">Anexo Atual</span>
                                             <span className="text-2xl font-black text-red-400">Anexo V — 15,5%</span>
                                           </div>
                                           <div className="text-center flex flex-col items-center justify-center">
                                             {migra ? (
                                               <>
                                                 <span className="text-[10px] text-slate-500 uppercase font-bold block">Economia Anual Projetada</span>
                                                 <span className="text-xl font-black text-emerald-400">{fmtCurrency(economiaReal)}</span>
                                                 <span className="text-[10px] text-emerald-600 font-semibold">Diferença de 9,5pp na alíquota</span>
                                               </>
                                             ) : (
                                               <>
                                                 <span className="text-[10px] text-slate-500 uppercase font-bold block">Falta para atingir 28%</span>
                                                 <span className="text-xl font-black text-amber-400">{(28 - fatorR).toFixed(2).replace(".", ",")}pp</span>
                                                 <span className="text-[10px] text-slate-500 font-semibold">Aumentar folha ou reduzir receita</span>
                                               </>
                                             )}
                                           </div>
                                           <div className="text-center">
                                             <span className="text-[10px] text-slate-500 uppercase font-bold block">Anexo {migra ? "Recomendado" : "Alvo"}</span>
                                             <span className={`text-2xl font-black ${migra ? "text-emerald-400" : "text-slate-500"}`}>Anexo III — 6,0%</span>
                                           </div>
                                         </div>
                                         {migra && (
                                           <div className="px-5 pb-5 space-y-2">
                                             <p className="text-[10px] font-bold text-slate-400 uppercase">Próximos Passos para Migração:</p>
                                             {["Emitir o PGDAS-D do mês seguinte já apontando para o Anexo III no campo de atividade.", "Reunir o demonstrativo de folha (SEFIP/eSocial) e receita bruta (DAS/PGDAS) dos últimos 12 meses.", "Comunicar formalmente ao contador para ajuste da classificação de CNAE e Anexo no portal do Simples.", "Monitorar mensalmente o Fator R para manter a elegibilidade ao Anexo III."].map((step, i) => (
                                               <div key={i} className="flex items-start gap-2 text-xs text-slate-300">
                                                 <span className="w-4 h-4 rounded-full bg-emerald-500/20 text-emerald-400 text-[9px] font-bold flex items-center justify-center shrink-0 mt-0.5">{i+1}</span>
                                                 <span>{step}</span>
                                               </div>
                                             ))}
                                           </div>
                                         )}
                                         {!migra && (
                                           <div className="px-5 pb-5 space-y-2">
                                             <p className="text-[10px] font-bold text-slate-400 uppercase">Estratégias para Atingir o Fator R de 28%:</p>
                                             {["Formalizar sócios como empregados CLT (pró-labore com vínculo) para aumentar a folha de pagamentos computada.", "Contratar colaboradores PJ para prestação de serviços intelectuais e incluir remuneração na base de cálculo do FGTS.", "Revisar se o pró-labore atual está sendo incluso corretamente no cálculo da folha dos 12 meses."].map((step, i) => (
                                               <div key={i} className="flex items-start gap-2 text-xs text-slate-300">
                                                 <span className="w-4 h-4 rounded-full bg-amber-500/20 text-amber-400 text-[9px] font-bold flex items-center justify-center shrink-0 mt-0.5">{i+1}</span>
                                                 <span>{step}</span>
                                               </div>
                                             ))}
                                           </div>
                                         )}
                                       </div>
                                     ) : (
                                       <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                         <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-4 text-center">
                                           <span className="text-[10px] font-bold text-red-400 uppercase block">Anexo V</span>
                                           <span className="text-3xl font-black text-red-400">15,5%</span>
                                           <span className="text-[10px] text-slate-500 block mt-1">Alíquota inicial — Impostos maiores</span>
                                         </div>
                                         <div className="bg-slate-900 border border-slate-700 rounded-xl p-4 text-center flex flex-col justify-center gap-1">
                                           <span className="text-[10px] font-bold text-slate-400 uppercase">Fator R = Folha 12m ÷ Receita 12m</span>
                                           <div className="text-2xl font-black text-sky-400">≥ 28%</div>
                                           <span className="text-[10px] text-slate-500">Preencha os campos acima para calcular</span>
                                         </div>
                                         <div className="bg-emerald-500/10 border border-emerald-500/20 rounded-xl p-4 text-center">
                                           <span className="text-[10px] font-bold text-emerald-400 uppercase block">Anexo III</span>
                                           <span className="text-3xl font-black text-emerald-400">6,0%</span>
                                           <span className="text-[10px] text-slate-500 block mt-1">Alíquota inicial — Impostos menores</span>
                                         </div>
                                       </div>
                                     )}

                                      <div className="space-y-2 pt-2 border-t border-slate-900">
                                        <label className="text-[9px] font-bold text-slate-500 uppercase tracking-wider block">
                                          Selecione um setor sujeito ao Fator R para simular:
                                        </label>
                                        <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                                          {FATOR_R_SECTORS.map((sec, i) => {
                                            const active = selectedFatorRSector === sec.name;
                                            return (
                                              <button
                                                key={i}
                                                type="button"
                                                onClick={() => selectSector(sec.name)}
                                                className={`border rounded-lg p-2.5 text-center text-[10px] font-bold transition-all ${
                                                  active
                                                    ? "bg-sky-500/20 border-sky-400 text-sky-300 ring-2 ring-sky-500/25"
                                                    : "bg-slate-900 border-slate-800 text-slate-400 hover:border-slate-700 hover:text-slate-200"
                                                }`}
                                              >
                                                {sec.name}
                                              </button>
                                            );
                                          })}
                                        </div>
                                      </div>

                                     {!isSimples && (
                                       <div className="bg-indigo-950/20 border border-indigo-500/20 rounded-xl p-4 text-xs text-indigo-300 font-semibold flex items-start gap-2">
                                         <Brain size={14} className="text-indigo-400 shrink-0 mt-0.5" />
                                         <span>Esta empresa está no <strong>Lucro Real</strong> — o Fator R não se aplica. O benefício equivalente é a <strong>Lei do Bem</strong>, que permite deduzir até 34% de IRPJ/CSLL sobre despesas de P&D. Use o Simulador Tributário para calcular a economia.</span>
                                       </div>
                                     )}

                                   </div>
                                 </div>
                               );
                             })()}

                            {/* Parecer Executivo */}
                            {parecer && (
                              <div className="bg-gradient-to-br from-indigo-950/30 to-slate-950 border border-indigo-900/30 rounded-2xl overflow-hidden">
                                <div className="px-5 py-4 border-b border-indigo-900/20 flex items-center gap-2">
                                  <Brain size={16} className="text-indigo-400" />
                                  <h5 className="font-extrabold text-white text-sm">Parecer Executivo — Gabriel (Agente Especialista)</h5>
                                  <span className="ml-auto text-[9px] font-bold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 px-2 py-0.5 rounded uppercase">Agente Gabriel</span>
                                </div>
                                <div className="p-5">
                                  <p className="text-slate-300 text-sm leading-relaxed font-medium">{parecer}</p>
                                </div>
                              </div>
                            )}

                            {/* Divida Ativa no Score Tab */}
                            {result.divida_ativa_uniao && result.divida_ativa_uniao.length > 0 && (
                              <div className="space-y-3">
                                <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                                  <ShieldAlert size={14} className="text-red-400" />
                                  Dívida Ativa da União (PGFN) — Alerta Fiscal Identificado
                                </h5>
                                {result.divida_ativa_uniao.map((d: any, i: number) => (
                                  <div key={i} className="bg-red-950/20 border border-red-500/30 rounded-xl p-4 flex flex-col md:flex-row items-start md:items-center justify-between gap-3">
                                    <div className="space-y-0.5">
                                      <span className="text-[10px] font-bold text-red-400 uppercase tracking-wider">Inscrição: {d.inscricao}</span>
                                      <p className="text-xs text-slate-300 font-semibold">{d.natureza || "Tributária"} — {d.situacao}</p>
                                    </div>
                                    <div className="text-right">
                                      <span className="text-xl font-extrabold text-red-400 font-mono">
                                        {new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(d.valor || 0)}
                                      </span>
                                      <p className="text-[10px] text-slate-500">Regularize via PERT-Digital no e-CAC</p>
                                    </div>
                                  </div>
                                ))}
                              </div>
                            )}

                            {/* Protestos em Cartórios no Score Tab */}
                            {(() => {
                              const protestos = result.protestos ?? result.risk_profile?.protestos ?? [];
                              if (protestos.length === 0) return null;
                              return (
                                <div className="space-y-3 mt-4">
                                  <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                                    <AlertTriangle size={14} className="text-rose-400" />
                                    Títulos Protestados em Cartórios (CENPROT) — Inadimplência Formalizada
                                  </h5>
                                  {protestos.map((p: any, i: number) => (
                                    <div key={i} className="bg-rose-950/25 border border-rose-500/35 rounded-xl p-4 flex flex-col md:flex-row items-start md:items-center justify-between gap-3">
                                      <div className="space-y-0.5">
                                        <span className="text-[10px] font-bold text-rose-400 uppercase tracking-wider">{p.cartorio}</span>
                                        <p className="text-xs text-slate-300 font-semibold">
                                          {p.documento_protestado} &bull; Data: {p.data_protesto} &bull; Status: <span className="underline font-bold text-rose-400">{p.status}</span>
                                        </p>
                                        {p.anuencia_solicitada && (
                                          <p className="text-[10px] text-amber-400/90 font-medium">Carta de anuência para cancelamento solicitada.</p>
                                        )}
                                      </div>
                                      <div className="text-right">
                                        <span className="text-xl font-extrabold text-rose-400 font-mono">
                                          {new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(p.valor || 0)}
                                        </span>
                                        <p className="text-[10px] text-slate-500">Regularizar diretamente no cartório de origem</p>
                                      </div>
                                    </div>
                                  ))}
                                </div>
                              );
                            })()}

                          </div>
                        );
                      })()}

                      {/* TAB 3: Reforma Tributária */}
                      {activeTab === "reforma" && result.reforma_tributaria && (
                        <div className="space-y-6">
                          <div className="border-l-4 border-sky-400 pl-3">
                            <h4 className="text-lg font-bold text-white">Impacto da Nova Reforma Tributária (IBS / CBS)</h4>
                            <p className="text-slate-400 text-xs mt-0.5">Análise preditiva de transição para o novo modelo de consumo (Emenda Constitucional 132/2023).</p>
                          </div>

                          {/* Parecer do Especialista */}
                          <div className="bg-slate-950 p-5 rounded-xl border border-sky-950/20 space-y-3">
                            <h5 className="text-xs font-bold text-sky-300 uppercase tracking-wider flex items-center gap-1.5">
                              <Scale size={14} className="text-sky-400" />
                              Parecer do Especialista em Direito Tributário
                            </h5>
                            <div className="text-slate-300 text-xs leading-relaxed space-y-2.5 font-medium">
                              <p>
                                O perfil do CNPJ analisado pertence ao setor de <strong>tecnologia e serviços integrados</strong>. Atualmente, sob o Lucro Presumido, a empresa desfruta de uma alíquota combinada de PIS/COFINS (cumulativo a 3,65%) e ISS municipal (5%), perfazendo uma carga nominal média sobre o faturamento de <strong>16,33%</strong>.
                              </p>
                              <p>
                                Com a entrada em vigor do IBS e CBS, a alíquota unificada de referência estimada será de <strong>26,50%</strong>. Nominalmente, isso representa um acréscimo tarifário expressivo para empresas de serviços. Entretanto, a reforma tributária introduz o regime de <strong>não-cumulatividade plena (crédito físico e financeiro amplo)</strong>. Isso significa que a sua empresa passará a ter direito a creditar-se sobre a aquisição de todos os seus insumos de tecnologia, locação de servidores (cloud), prestadores de serviços de desenvolvimento contratados e aquisição de equipamentos de hardware.
                              </p>
                              <p>
                                <strong>Recomendação Estratégica:</strong> Para mitigar a elevação nominal, a empresa deve implantar um mapeamento contábil rigoroso e transferir seus contratos de prestação de serviços com terceiros para fornecedores enquadrados no Lucro Real/Reforma. Desta forma, a apuração de créditos compensará o aumento da alíquota na saída. Além disso, destacamos que as desonerações federais da <strong>Lei do Bem permanecem vigentes</strong> pós-reforma.
                              </p>
                            </div>
                          </div>

                          {/* Aliquot stats comparison cards */}
                          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            {/* Aliquot box */}
                            <div className="bg-slate-950 p-5 rounded-xl border border-slate-900 flex flex-col justify-center items-center text-center">
                              <span className="text-xs text-slate-500 font-bold uppercase tracking-wider block mb-2">Alíquota Unificada Estimada</span>
                              <span className="text-4xl font-extrabold text-amber-500 tracking-tight font-mono">{result.reforma_tributaria.aliquota_estimada_ibs_cbs}</span>
                              <span className="text-[10px] text-slate-500 font-bold mt-2 uppercase">IBS + CBS MÁXIMO (CONSUMO)</span>
                            </div>

                            {/* Impact status */}
                            <div className="bg-slate-950 p-5 rounded-xl border border-slate-900 flex flex-col justify-center items-center text-center">
                              <span className="text-xs text-slate-500 font-bold uppercase tracking-wider block mb-2">Impacto Geral Projetado</span>
                              <span className="text-xl font-extrabold text-sky-400 uppercase tracking-wide px-3 py-1 bg-sky-950/20 border border-sky-900/30 rounded-lg">
                                {result.reforma_tributaria.impacto_geral}
                              </span>
                              <span className="text-[10px] text-slate-500 font-bold mt-3 uppercase">HÍBRIDO (2026-2033)</span>
                            </div>

                            {/* Select Tax */}
                            <div className="bg-slate-950 p-5 rounded-xl border border-slate-900 flex flex-col justify-center items-center text-center">
                              <span className="text-xs text-slate-500 font-bold uppercase tracking-wider block mb-2">Imposto Seletivo</span>
                              <span className={`text-sm font-extrabold uppercase px-3 py-1 rounded-lg ${result.reforma_tributaria.imposto_seletivo === "Inaplicável" ? "bg-slate-900 text-slate-500 border border-slate-800" : "bg-red-500/10 text-red-400 border border-red-500/20"}`}>
                                {result.reforma_tributaria.imposto_seletivo}
                              </span>
                              <span className="text-[10px] text-slate-500 font-bold mt-3 uppercase">TRIBUTAÇÃO SOBRE SAÚDE/FUMO</span>
                            </div>
                          </div>

                          {/* Comparativo de Tributação Nominal Pré vs Pós Reforma */}
                          <div className="bg-slate-950 p-5 rounded-xl border border-slate-900 space-y-4">
                            <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider border-b border-slate-900 pb-2">Comparativo de Alíquotas Nominais (Pré vs. Pós Reforma)</h5>
                            <div className="overflow-x-auto">
                              <table className="w-full text-left text-xs border-collapse min-w-[500px]">
                                <thead>
                                  <tr className="border-b border-slate-900 text-slate-500 font-bold uppercase text-[9px]">
                                    <th className="pb-2">Grupo de Tributos</th>
                                    <th className="pb-2">Tributos Antigos (Pré-Reforma)</th>
                                    <th className="pb-2 text-right">Carga Antiga</th>
                                    <th className="pb-2">Novos Tributos (Pós-Reforma)</th>
                                    <th className="pb-2 text-right">Carga Nova (Simulada)</th>
                                  </tr>
                                </thead>
                                <tbody className="font-mono text-slate-300">
                                  <tr className="border-b border-slate-900/40">
                                    <td className="py-2.5 font-sans font-semibold text-white">Impostos Estaduais/Municipais</td>
                                    <td>ICMS (Estadual) + ISS (Municipal)</td>
                                    <td className="text-right font-bold">5.00% a 18.00%</td>
                                    <td className="text-sky-400 font-sans font-semibold">IBS (Imposto sobre Bens e Serviços)</td>
                                    <td className="text-right font-bold text-sky-400">17.70% (Estimada)</td>
                                  </tr>
                                  <tr className="border-b border-slate-900/40">
                                    <td className="py-2.5 font-sans font-semibold text-white">Contribuições Federais</td>
                                    <td>PIS (Federal) + COFINS (Federal) + IPI</td>
                                    <td className="text-right font-bold">3.65% a 9.25%</td>
                                    <td className="text-sky-400 font-sans font-semibold">CBS (Contribuição sobre Bens e Serviços)</td>
                                    <td className="text-right font-bold text-sky-400">8.80% (Fixado)</td>
                                  </tr>
                                  <tr className="border-b border-slate-900/40">
                                    <td className="py-2.5 font-sans font-semibold text-white">Tributação de Renda</td>
                                    <td>IRPJ (Renda) + CSLL (Contribuição Social)</td>
                                    <td className="text-right font-bold">34.00% (Real/Pres)</td>
                                    <td className="text-slate-400">Mantido sem alteração imediata</td>
                                    <td className="text-right font-bold text-slate-400">34.00%</td>
                                  </tr>
                                </tbody>
                              </table>
                            </div>
                          </div>

                          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            {/* Pontos Positivos */}
                            <div className="bg-slate-950 p-5 rounded-xl border border-slate-900 space-y-4">
                              <h5 className="text-xs font-bold text-emerald-400 uppercase tracking-wider border-b border-slate-900 pb-2 flex items-center gap-1.5">
                                <CheckCircle2 size={14} />
                                Oportunidades & Impactos Positivos
                              </h5>
                              <ul className="space-y-2.5">
                                {result.reforma_tributaria.pontos_positivos.map((p: string, idx: number) => (
                                  <li key={idx} className="text-xs text-slate-300 flex items-start gap-2 leading-relaxed font-semibold">
                                    <span className="text-emerald-500 font-extrabold mt-0.5">✓</span>
                                    <span>{p}</span>
                                  </li>
                                ))}
                              </ul>
                            </div>

                            {/* Pontos Negativos */}
                            <div className="bg-slate-950 p-5 rounded-xl border border-slate-900 space-y-4">
                              <h5 className="text-xs font-bold text-amber-400 uppercase tracking-wider border-b border-slate-900 pb-2 flex items-center gap-1.5">
                                <AlertTriangle size={14} />
                                Riscos & Pontos de Atenção
                              </h5>
                              <ul className="space-y-2.5">
                                {result.reforma_tributaria.pontos_negativos.map((p: string, idx: number) => (
                                  <li key={idx} className="text-xs text-slate-300 flex items-start gap-2 leading-relaxed font-semibold">
                                    <span className="text-amber-500 font-extrabold mt-0.5">!</span>
                                    <span>{p}</span>
                                  </li>
                                ))}
                              </ul>
                            </div>
                          </div>

                          {/* Preparação Contábil para a Transição */}
                          <div className="bg-slate-950 p-5 rounded-xl border border-slate-900 space-y-3">
                            <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider border-b border-slate-900 pb-2">Plano de Preparação Contábil para a Transição (2026-2033)</h5>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs pt-1">
                              <div className="bg-slate-900 p-4 rounded border border-slate-850 space-y-1">
                                <span className="text-sky-400 font-bold text-[11px] block">1. Auditoria de Fornecedores</span>
                                Mapeie e renegocie com prestadores de serviço e fornecedores enquadrados no regime de não-cumulatividade plena, garantindo que as notas de compra tragam destaque de CBS/IBS para compensar as saídas.
                              </div>
                              <div className="bg-slate-900 p-4 rounded border border-slate-850 space-y-1">
                                <span className="text-sky-400 font-bold text-[11px] block">2. Parametrização Fiscal (Sistemas)</span>
                                Adequar os sistemas de faturamento da empresa (ERP) para suportar o período híbrido (cálculo paralelo dos impostos vigentes + IBS/CBS com alíquotas teste de 0,1% e 0,9%).
                              </div>
                              <div className="bg-slate-900 p-4 rounded border border-slate-850 space-y-1">
                                <span className="text-sky-400 font-bold text-[11px] block">3. Estruturação Contratual</span>
                                Revisar as cláusulas de preços contratuais prevendo repasses inflacionários ou reajustes decorrentes do acréscimo nominal de ISS municipal para o novo IBS estadual.
                              </div>
                            </div>
                          </div>

                        </div>
                      )}

                      {/* TAB CYBER: Pegada Digital & Cyber Threat Intelligence */}
                      {activeTab === "cyber" && (() => {
                        const cyber = result.cyber_intel;
                        if (!cyber) return (
                          <div className="flex flex-col items-center justify-center py-16 space-y-3 text-slate-500">
                            <ShieldAlert size={40} className="opacity-30" />
                            <p className="text-sm font-semibold">Varredura de Cyber Intelig\u00eancia n\u00e3o dispon\u00edvel para este CNPJ.</p>
                            <p className="text-xs">O domínio corporativo não pôde ser inferido do QSA. Nenhuma chave de API é necessária — o motor usa crt.sh, ipinfo.io e análise DNS gratuitos.</p>
                          </div>
                        );
                        const cs = cyber.cyber_score ?? 100;
                        const csColor = cs < 40 ? "text-red-400 border-red-500" : cs < 70 ? "text-amber-400 border-amber-500" : "text-emerald-400 border-emerald-500";
                        const csNivel = cs < 40 ? "CR\u00cdTICO" : cs < 70 ? "ATEN\u00c7\u00c3O" : "PROTEGIDO";
                        const csNivelBg = cs < 40 ? "bg-red-500/10 text-red-400 border-red-500/30" : cs < 70 ? "bg-amber-500/10 text-amber-400 border-amber-500/30" : "bg-emerald-500/10 text-emerald-400 border-emerald-500/30";
                        const sevColor: Record<string, string> = { "CR\u00cdTICO": "text-red-400 bg-red-500/10 border-red-500/30", "ALTO": "text-orange-400 bg-orange-500/10 border-orange-500/30", "M\u00c9DIO": "text-amber-400 bg-amber-500/10 border-amber-500/30", "OK": "text-emerald-400 bg-emerald-500/10 border-emerald-500/30" };
                        const riskDot: Record<string, string> = { "CR\u00cdTICO": "bg-red-500", "ALTO": "bg-orange-500", "M\u00c9DIO": "bg-amber-500", "OK": "bg-emerald-500" };
                        return (
                          <div className="space-y-6">
                            {/* Header */}
                            <div className="border-l-4 border-rose-600 pl-3">
                              <h4 className="text-lg font-bold text-white flex items-center gap-2">
                                <ShieldAlert size={20} className="text-rose-500" />
                                Pegada Digital & Cyber Threat Intelligence
                              </h4>
                              <p className="text-slate-400 text-xs mt-0.5">Mapeamento passivo da superf\u00edcie de ataque, vaz\u00f5es de credenciais na Dark Web e exposi\u00e7\u00f5es OSINT de fontes abertas.</p>
                            </div>

                            {/* Cyber Score + Contadores */}
                            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                              {/* Gauge */}
                              <div className="bg-gradient-to-br from-rose-950/40 to-slate-950 border border-rose-900/40 rounded-2xl p-5 flex flex-col items-center justify-center text-center space-y-2 col-span-1">
                                <span className="text-[9px] font-bold text-slate-500 uppercase tracking-widest">Cyber Score</span>
                                <div className={`w-20 h-20 rounded-full border-[5px] flex flex-col items-center justify-center ${csColor}`}>
                                  <span className="text-2xl font-black">{cs}</span>
                                  <span className="text-[8px] text-slate-500">/100</span>
                                </div>
                                <span className={`text-[10px] font-extrabold px-2 py-0.5 rounded-full border uppercase ${csNivelBg}`}>{csNivel}</span>
                              </div>
                              {/* Stats */}
                              {[
                                { label: "Portas Expostas", val: cyber.attack_surface?.portas_expostas?.filter((p: any) => p.risco !== "OK").length ?? 0, color: "text-red-400", icon: "🔓" },
                                { label: "Credenciais Vazadas", val: cyber.dark_web?.credenciais_vazadas ?? 0, color: "text-rose-400", icon: "🕵" },
                                { label: "Achados OSINT", val: cyber.osint_findings?.length ?? 0, color: "text-orange-400", icon: "📄" },
                              ].map((stat, i) => (
                                <div key={i} className="bg-slate-950 border border-slate-800 rounded-2xl p-5 flex flex-col items-center justify-center text-center space-y-1">
                                  <span className="text-2xl">{stat.icon}</span>
                                  <span className={`text-3xl font-black ${stat.color}`}>{stat.val}</span>
                                  <span className="text-[10px] text-slate-500 font-semibold uppercase">{stat.label}</span>
                                </div>
                              ))}
                            </div>

                            {/* Attack Surface */}
                            <div className="space-y-3">
                              <h5 className="text-xs font-extrabold text-white uppercase tracking-wider flex items-center gap-2">
                                <span className="w-2 h-2 rounded-full bg-rose-500 animate-pulse" />
                                Attack Surface Map — Infraestrutura Exposta
                              </h5>
                              <div className="bg-slate-950 border border-slate-800 rounded-2xl overflow-hidden">
                                <div className="bg-slate-900/60 px-4 py-2.5 border-b border-slate-800 grid grid-cols-4 text-[9px] font-bold text-slate-500 uppercase">
                                  <span>Porta / Servi\u00e7o</span><span>IP Identificado</span><span>CVE / Detalhe</span><span className="text-right">Severidade</span>
                                </div>
                                {cyber.attack_surface?.portas_expostas?.map((p: any, i: number) => (
                                  <div key={i} className={`px-4 py-3.5 border-b border-slate-900/50 grid grid-cols-4 items-center gap-2 hover:bg-slate-900/30 transition-colors ${p.risco !== "OK" ? "" : "opacity-60"}`}>
                                    <div className="flex items-center gap-2">
                                      <div className={`w-2 h-2 rounded-full shrink-0 ${riskDot[p.risco] ?? "bg-slate-500"} ${p.risco === "CR\u00cdTICO" ? "animate-pulse" : ""}`} />
                                      <div>
                                        <span className="font-mono font-extrabold text-white text-xs">{p.porta}</span>
                                        <span className="text-slate-400 text-[11px] block">{p.servico}</span>
                                      </div>
                                    </div>
                                    <span className="font-mono text-[11px] text-slate-400">{p.ip}</span>
                                    <span className="text-[10px] text-slate-500 leading-snug">{p.cve || "—"}</span>
                                    <span className={`text-[9px] font-extrabold px-2 py-0.5 rounded-full border text-right ml-auto ${sevColor[p.risco] ?? "text-slate-400 bg-slate-800 border-slate-700"}`}>{p.risco}</span>
                                  </div>
                                ))}
                                {/* Tecnologias Legadas */}
                                {cyber.attack_surface?.tecnologias_legadas?.map((t: string, i: number) => (
                                  <div key={`t-${i}`} className="px-4 py-3 border-b border-slate-900/50 flex items-center gap-3 bg-amber-950/10">
                                    <div className="w-2 h-2 rounded-full bg-amber-500 shrink-0" />
                                    <span className="text-[11px] text-amber-300 font-semibold">{t}</span>
                                    <span className="ml-auto text-[9px] font-bold text-amber-400 bg-amber-500/10 border border-amber-500/20 px-2 py-0.5 rounded-full">LEGADO</span>
                                  </div>
                                ))}
                                {/* SSL */}
                                <div className={`px-4 py-3 flex items-center gap-3 ${!cyber.attack_surface?.ssl_valido ? "bg-red-950/20" : "bg-emerald-950/10"}`}>
                                  <div className={`w-2 h-2 rounded-full ${!cyber.attack_surface?.ssl_valido ? "bg-red-500" : "bg-emerald-500"}`} />
                                  <span className="text-[11px] text-slate-300 font-semibold">
                                    Certificado SSL/TLS — {cyber.attack_surface?.ssl_valido ? "V\u00e1lido" : "Expirado/Inv\u00e1lido"}
                                    {cyber.attack_surface?.ssl_expira_em ? ` (expira em ${cyber.attack_surface.ssl_expira_em})` : ""}
                                  </span>
                                  <span className={`ml-auto text-[9px] font-bold px-2 py-0.5 rounded-full border ${!cyber.attack_surface?.ssl_valido ? "text-red-400 bg-red-500/10 border-red-500/20" : cyber.attack_surface?.ssl_expira_em?.includes("4") ? "text-amber-400 bg-amber-500/10 border-amber-500/20" : "text-emerald-400 bg-emerald-500/10 border-emerald-500/20"}`}>
                                    {!cyber.attack_surface?.ssl_valido ? "CR\u00cdTICO" : cyber.attack_surface?.ssl_expira_em?.includes("4") ? "ATEN\u00c7\u00c3O" : "OK"}
                                  </span>
                                </div>
                              </div>
                            </div>

                            {/* Dark Web Monitor */}
                            <div className="space-y-3">
                              <h5 className="text-xs font-extrabold text-white uppercase tracking-wider flex items-center gap-2">
                                <span className="w-2 h-2 rounded-full bg-purple-500" />
                                Dark Web Credential Monitor — Vaz\u00f5es Identificadas
                              </h5>
                              <div className="bg-slate-950 border border-red-900/30 rounded-2xl overflow-hidden">
                                <div className="bg-red-950/20 px-4 py-3 border-b border-red-900/20 flex items-center justify-between gap-2">
                                  <span className="text-red-400 font-bold text-xs">Vazamentos de Credenciais Corporativas</span>
                                  <span className="text-[9px] font-extrabold text-red-400 bg-red-500/10 border border-red-500/20 px-2 py-0.5 rounded-full">{cyber.dark_web?.credenciais_vazadas} VAZAMENTOS DETECTADOS</span>
                                </div>
                                <div className="p-4 space-y-4">
                                  <p className="text-xs text-slate-400 leading-relaxed">
                                    Identificamos indícios de vazamento de credenciais associadas aos domínios da empresa em bases históricas expostas e fóruns cibernéticos. Para resguardar a privacidade e a segurança da informação, a listagem individualizada de e-mails não é exibida diretamente no painel estratégico.
                                  </p>
                                  <div className="space-y-2">
                                    <div className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Bases de Dados / Eventos de Vazamento</div>
                                    {cyber.dark_web?.breaches?.map((b: any, i: number) => (
                                      <div key={i} className="flex items-start justify-between gap-3 p-2.5 bg-slate-900 border border-slate-800 rounded-lg">
                                        <div>
                                          <span className="text-xs font-bold text-white block">{b.fonte}</span>
                                          <span className="text-[10px] text-slate-500">{b.data} &mdash; {b.tipo}</span>
                                        </div>
                                        <span className={`text-[9px] font-extrabold px-2 py-0.5 rounded-full border shrink-0 ${sevColor[b.severidade] ?? ""}`}>{b.severidade}</span>
                                      </div>
                                    ))}
                                  </div>
                                </div>
                              </div>
                            </div>

                            {/* OSINT Surface Web */}
                            <div className="space-y-3">
                              <h5 className="text-xs font-extrabold text-white uppercase tracking-wider flex items-center gap-2">
                                <span className="w-2 h-2 rounded-full bg-orange-500" />
                                OSINT Surface Web — Documentos & Configs Indexados
                              </h5>
                              <div className="bg-slate-950 border border-slate-800 rounded-2xl overflow-hidden">
                                <div className="bg-slate-900/60 px-4 py-2.5 border-b border-slate-800 grid grid-cols-3 text-[9px] font-bold text-slate-500 uppercase">
                                  <span>Tipo de Achado</span><span>Arquivo / Recurso</span><span className="text-right">Severidade</span>
                                </div>
                                {cyber.osint_findings?.map((o: any, i: number) => (
                                  <div key={i} className="px-4 py-3.5 border-b border-slate-900/50 grid grid-cols-3 items-center gap-2 hover:bg-slate-900/30 transition-colors">
                                    <span className="text-[10px] font-bold text-slate-400 bg-slate-800 px-2 py-0.5 rounded w-fit">{o.tipo}</span>
                                    <span className="text-[11px] text-slate-300 font-semibold leading-snug truncate">{o.nome}</span>
                                    <span className={`text-[9px] font-extrabold px-2 py-0.5 rounded-full border text-right ml-auto w-fit ${sevColor[o.severidade] ?? ""}`}>{o.severidade}</span>
                                  </div>
                                ))}
                              </div>
                            </div>

                            {/* Plano de Mitigação */}
                            <div className="space-y-3">
                              <h5 className="text-xs font-extrabold text-white uppercase tracking-wider flex items-center gap-2">
                                <ShieldCheck size={14} className="text-emerald-400" />
                                Plano de Mitigação — Ações Prioritizadas
                              </h5>
                              <div className="space-y-2">
                                {cyber.recomendacoes?.map((r: any, i: number) => (
                                  <div key={i} className={`flex items-start gap-3 p-3.5 rounded-xl border ${r.prioridade === "URGENTE" ? "bg-red-950/20 border-red-500/30" : r.prioridade === "ALTO" ? "bg-orange-950/20 border-orange-500/30" : "bg-amber-950/20 border-amber-500/30"}`}>
                                    <span className={`text-[9px] font-extrabold px-2 py-1 rounded border shrink-0 mt-0.5 ${r.prioridade === "URGENTE" ? "text-red-400 bg-red-500/10 border-red-500/30" : r.prioridade === "ALTO" ? "text-orange-400 bg-orange-500/10 border-orange-500/30" : "text-amber-400 bg-amber-500/10 border-amber-500/30"}`}>{r.prioridade}</span>
                                    <p className="text-xs text-slate-300 font-semibold leading-relaxed">{r.acao}</p>
                                  </div>
                                ))}
                              </div>
                            </div>

                            {/* Aviso Legal */}
                            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-start gap-3 text-xs text-slate-500">
                              <ShieldAlert size={14} className="text-slate-600 shrink-0 mt-0.5" />
                              <p>Este m\u00f3dulo realiza apenas <strong className="text-slate-400">varredura passiva</strong> de fontes p\u00fablicas e registros de transpar\u00eancia (crt.sh, ipinfo.io, GreyNoise, dns, socket). Nenhum ativo da empresa \u00e9 escaneado ativamente (sem port scan intrusivo, sem testes de penetra\u00e7\u00e3o). Compliance com LGPD e Marco Civil da Internet.</p>
                            </div>
                          </div>
                        );
                      })()}

                      {/* TAB INCENTIVES: Alavancagem Financeira & Incentivos Fiscais */}
                      {activeTab === "incentives" && (() => {
                        const inc = result.incentivos_financiamento;
                        if (!inc) return (
                          <div className="flex flex-col items-center justify-center py-16 space-y-3 text-slate-500">
                            <ShieldAlert size={40} className="opacity-30" />
                            <p className="text-sm font-semibold">Módulo de Alavancagem Financeira não carregado.</p>
                            <p className="text-xs">Consulte um CNPJ válido para carregar as oportunidades fiscais e de crédito.</p>
                          </div>
                        );

                        const score = inc.score_governanca ?? 100;
                        const scoreBg = score < 50 ? "bg-red-500/10 text-red-400 border-red-500/30" : score < 80 ? "bg-amber-500/10 text-amber-400 border-amber-500/30" : "bg-emerald-500/10 text-emerald-400 border-emerald-500/30";
                        const scoreNivel = score < 50 ? "CRÍTICO (Gaps Elevados)" : score < 80 ? "REGULAR (Aproveitamento Parcial)" : "OTIMIZADO (Excelente Aproveitamento)";
                        const sevColor: Record<string, string> = { "CRÍTICO": "text-red-400 bg-red-500/10 border-red-500/30", "ALTO": "text-orange-400 bg-orange-500/10 border-orange-500/30", "MÉDIO": "text-amber-400 bg-amber-500/10 border-amber-500/30", "OK": "text-emerald-400 bg-emerald-500/10 border-emerald-500/30", "N/A": "text-slate-400 bg-slate-800/10 border-slate-800" };

                        return (
                          <div className="space-y-8 animate-fadeIn">
                            {/* Top Summary Banner */}
                            <div className="bg-gradient-to-br from-slate-900 via-slate-950 to-slate-900 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-center justify-between gap-6 shadow-2xl">
                              <div className="space-y-2 max-w-xl text-left">
                                <span className="text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2.5 py-1 rounded-full uppercase tracking-wider block w-fit">
                                  Módulo 6 — Governança Tributária &amp; Crédito
                                </span>
                                <h4 className="text-xl font-black text-white leading-tight">Alavancagem Financeira e Mapeamento Global de Incentivos</h4>
                                <p className="text-xs text-slate-400 leading-relaxed">{inc.resumo}</p>
                              </div>
                              <div className={`shrink-0 border rounded-2xl p-5 text-center flex flex-col justify-center items-center gap-1.5 w-full md:w-44 ${scoreBg}`}>
                                <span className="text-[9px] font-bold uppercase tracking-widest text-slate-400">Score de Governança</span>
                                <span className="text-4xl font-black font-mono leading-none">{score}/100</span>
                                <span className="text-[9px] font-bold leading-tight mt-0.5">{scoreNivel}</span>
                              </div>
                            </div>

                            {/* Two Column Section: Loans & Gaps */}
                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                              {/* 1. Empréstimos e Financiamentos (BNDES/FINEP) */}
                              <div className="space-y-4 text-left">
                                <h5 className="text-xs font-extrabold text-white uppercase tracking-wider flex items-center gap-2">
                                  <span className="w-2 h-2 rounded-full bg-emerald-500" />
                                  Linhas de Crédito &amp; Financiamentos Ativos (OSINT)
                                </h5>
                                <div className="space-y-3">
                                  {inc.financiamentos && inc.financiamentos.length > 0 ? (
                                    inc.financiamentos.map((f: any, idx: number) => (
                                      <div key={idx} className="bg-slate-950 border border-slate-800 rounded-2xl overflow-hidden shadow-md">
                                        <div className="bg-slate-900/60 px-4 py-3 border-b border-slate-800 flex items-center justify-between gap-2">
                                          <div className="flex items-center gap-2">
                                            <span className={`text-[9px] font-extrabold px-2 py-0.5 rounded border ${
                                              f.fonte === "FINEP" ? "text-sky-400 bg-sky-500/10 border-sky-500/20" : "text-emerald-400 bg-emerald-500/10 border-emerald-500/20"
                                            }`}>
                                              {f.fonte}
                                            </span>
                                            <span className="text-xs font-bold text-white">{f.produto}</span>
                                          </div>
                                          <span className="text-[10px] text-slate-500 font-mono">{f.ano || ""}</span>
                                        </div>
                                        <div className="p-4 flex justify-between items-center gap-4">
                                          <div className="text-left">
                                            <span className="text-[10px] text-slate-500 uppercase block font-bold">Valor Contratado</span>
                                            <span className="text-lg font-black text-white font-mono">
                                              {f.valor ? f.valor.toLocaleString("pt-BR", { style: "currency", currency: "BRL" }) : "N/A"}
                                            </span>
                                          </div>
                                          <div className="text-right">
                                            {f.taxa && (
                                              <div>
                                                <span className="text-[9px] text-slate-500 uppercase block font-bold">Encargos/Taxa</span>
                                                <span className="text-xs font-extrabold text-slate-300 font-mono">{f.taxa}</span>
                                              </div>
                                            )}
                                            {f.tipo && (
                                              <div>
                                                <span className="text-[9px] text-slate-500 uppercase block font-bold">Modalidade</span>
                                                <span className="text-xs font-bold text-slate-400">{f.tipo}</span>
                                              </div>
                                            )}
                                            <span className="inline-block mt-1 text-[9px] font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
                                              {f.status || "Ativa"}
                                            </span>
                                          </div>
                                        </div>
                                      </div>
                                    ))
                                  ) : (
                                    <div className="bg-slate-950 border border-slate-800 rounded-2xl p-8 text-center text-slate-500">
                                      Nenhuma operação de crédito identificada em portais de transparência pública (BNDES/FINEP).
                                    </div>
                                  )}
                                </div>
                              </div>

                              {/* 2. Alertas de Oportunidades Críticas (Gaps) */}
                              <div className="space-y-4 text-left">
                                <h5 className="text-xs font-extrabold text-white uppercase tracking-wider flex items-center gap-2">
                                  <span className="w-2 h-2 rounded-full bg-rose-500" />
                                  Gap Analysis — Desvios &amp; Oportunidades de Economia
                                </h5>
                                <div className="space-y-3">
                                  {inc.gap_analysis && inc.gap_analysis.some((g: any) => g.tem_direito && g.usa !== "OK") ? (
                                    inc.gap_analysis.filter((g: any) => g.tem_direito && g.usa !== "OK").map((g: any, idx: number) => {
                                      const crit = g.urgencia === "CRÍTICO" ? "border-red-500/30 bg-red-950/10" : "border-orange-500/30 bg-orange-950/10";
                                      const critText = g.urgencia === "CRÍTICO" ? "text-red-400 bg-red-500/10 border-red-500/30" : "text-orange-400 bg-orange-500/10 border-orange-500/30";
                                      return (
                                        <div key={idx} className={`border rounded-2xl p-4.5 space-y-3 shadow-md text-left ${crit}`}>
                                          <div className="flex items-center justify-between gap-2">
                                            <div className="flex items-center gap-2">
                                              <span className={`text-[9px] font-extrabold px-2 py-0.5 rounded border ${critText}`}>
                                                {g.urgencia}
                                              </span>
                                              <span className="text-xs font-extrabold text-white">{g.incentivo}</span>
                                            </div>
                                            {g.impacto_nao_aproveitado > 0 && (
                                              <div className="text-right">
                                                <span className="text-[9px] text-slate-400 block font-bold">Impacto Estimado</span>
                                                <span className="text-sm font-black text-rose-400 font-mono">
                                                  {g.impacto_nao_aproveitado.toLocaleString("pt-BR", { style: "currency", currency: "BRL" })}/ano
                                                </span>
                                              </div>
                                            )}
                                          </div>
                                          <p className="text-xs text-slate-300 font-medium leading-relaxed">{g.acao}</p>
                                        </div>
                                      );
                                    })
                                  ) : (
                                    <div className="bg-emerald-950/10 border border-emerald-500/20 text-emerald-400 rounded-2xl p-6 text-center text-xs font-semibold">
                                      ✓ Excelente conformidade fiscal! Todos os incentivos qualificados estão sendo aproveitados pela empresa.
                                    </div>
                                  )}
                                </div>
                              </div>
                            </div>

                            {/* 3. Tabela Comparativa Geral Direito x Uso */}
                            <div className="space-y-4 text-left">
                              <h5 className="text-xs font-extrabold text-white uppercase tracking-wider flex items-center gap-2">
                                <span className="w-2 h-2 rounded-full bg-sky-500" />
                                Mapeamento Global de Elegibilidade Tributária (Direito x Uso)
                              </h5>
                              <div className="bg-slate-950 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
                                <div className="overflow-x-auto">
                                  <table className="w-full text-left border-collapse">
                                    <thead>
                                      <tr className="bg-slate-900 border-b border-slate-800 text-[10px] font-bold text-slate-500 uppercase tracking-wider">
                                        <th className="px-5 py-3">Incentivo Mapeado</th>
                                        <th className="px-5 py-3">Elegibilidade</th>
                                        <th className="px-5 py-3">Status de Uso</th>
                                        <th className="px-5 py-3 text-right">Perda Projetada</th>
                                      </tr>
                                    </thead>
                                    <tbody>
                                      {inc.gap_analysis && inc.gap_analysis.map((g: any, idx: number) => (
                                        <tr key={idx} className="border-b border-slate-900 hover:bg-slate-900/30 transition-colors">
                                          <td className="px-5 py-3.5">
                                            <span className="text-xs font-bold text-white block">{g.incentivo}</span>
                                            <span className="text-[10px] text-slate-500 block max-w-md truncate">{g.acao}</span>
                                          </td>
                                          <td className="px-5 py-3.5">
                                            <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                                              g.tem_direito ? "text-emerald-400 bg-emerald-500/10 border-emerald-500/20" : "text-slate-500 bg-slate-800/10 border-slate-800"
                                            }`}>
                                              {g.tem_direito ? "ELEGÍVEL" : "NÃO ELEGÍVEL"}
                                            </span>
                                          </td>
                                          <td className="px-5 py-3.5">
                                            <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${sevColor[g.usa] ?? "text-slate-500 bg-slate-800/10 border-slate-800"}`}>
                                              {g.usa || "N/A"}
                                            </span>
                                          </td>
                                          <td className="px-5 py-3.5 text-right font-mono text-xs font-black text-slate-300 font-mono">
                                            {g.impacto_nao_aproveitado > 0 ? (
                                              <span className="text-rose-400">
                                                {g.impacto_nao_aproveitado.toLocaleString("pt-BR", { style: "currency", currency: "BRL" })}
                                              </span>
                                            ) : "R$ 0,00"}
                                          </td>
                                        </tr>
                                      ))}
                                    </tbody>
                                  </table>
                                </div>
                              </div>
                            </div>

                            {/* 4. Auditoria Fiscal Ativa via SPED (Upload) */}
                            <div className="space-y-4 text-left">
                              <h5 className="text-xs font-extrabold text-white uppercase tracking-wider flex items-center gap-2">
                                <span className="w-2 h-2 rounded-full bg-indigo-500" />
                                Auditoria Fiscal Ativa — Upload de Arquivos SPED
                              </h5>
                              <div className="bg-slate-950 border border-slate-800 rounded-2xl p-6 space-y-4 shadow-xl">
                                <p className="text-xs text-slate-400 leading-relaxed">
                                  Faça o upload do arquivo da escrituração contábil ou fiscal (ECF Bloco M/N/J, EFD-Contribuições ou EFD ICMS/IPI) para auditar se o aproveitamento dos incentivos está correto nos sistemas e corrigir desvios na DCTF/ECF.
                                </p>
                                
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                  {[
                                    { type: "ECF", label: "Upload ECF (LALUR/LACS)", desc: "Detecta Lei do Bem, PAT e passivos" },
                                    { type: "EFD_C", label: "Upload EFD-Contribuições", desc: "Varre CSTs de isenção e suspensão" },
                                    { type: "EFD_I", label: "Upload EFD ICMS/IPI", desc: "Identifica créditos presumidos estaduais" }
                                  ].map((up) => (
                                    <div key={up.type} className="border border-slate-800 hover:border-slate-700 bg-slate-900/40 p-4 rounded-xl flex flex-col justify-between items-start gap-4 transition-all">
                                      <div className="text-left">
                                        <span className="text-xs font-bold text-white block">{up.label}</span>
                                        <span className="text-[10px] text-slate-500 leading-relaxed block mt-0.5">{up.desc}</span>
                                      </div>
                                      <label className="w-full text-center bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-bold py-2 rounded-lg cursor-pointer transition-all border border-slate-700 block">
                                        Selecionar Arquivo
                                        <input
                                          type="file"
                                          accept=".txt,.txt.gz,.sped"
                                          onChange={handleSpedUpload}
                                          className="hidden"
                                          disabled={spedUploading}
                                        />
                                      </label>
                                    </div>
                                  ))}
                                </div>

                                {spedUploading && (
                                  <div className="flex items-center gap-3 bg-slate-900 border border-slate-800 rounded-xl p-4.5 animate-pulse text-left">
                                    <div className="w-4 h-4 rounded-full border-2 border-indigo-500 border-t-transparent animate-spin shrink-0" />
                                    <span className="text-xs text-indigo-300 font-semibold">Processando arquivo {spedFileUploaded}... Executando validação de blocos fiscais.</span>
                                  </div>
                                )}

                                {spedAuditResult && (
                                  <div className={`border rounded-xl p-4 flex items-start gap-3 text-xs leading-relaxed text-left ${
                                    spedAuditResult.status === "success" 
                                      ? "bg-emerald-950/20 border-emerald-500/30 text-emerald-300"
                                      : "bg-red-950/20 border-red-500/30 text-red-300"
                                  }`}>
                                    <span className="text-base shrink-0 mt-0.5">
                                      {spedAuditResult.status === "success" ? "✓" : "✗"}
                                    </span>
                                    <div>
                                      <p className="font-bold">{spedAuditResult.message}</p>
                                      {spedAuditResult.timestamp && (
                                        <span className="text-[10px] text-slate-500 font-mono block mt-1">Horário de processamento: {spedAuditResult.timestamp}</span>
                                      )}
                                    </div>
                                  </div>
                                )}
                              </div>
                            </div>
                          </div>
                        );
                      })()}

                      {/* TAB 4: Compliance, Riscos & Fontes */}
                      {activeTab === "compliance" && (
                        <div className="space-y-6">
                          <div className="border-l-4 border-sky-400 pl-3">
                            <h4 className="text-lg font-bold text-white">Auditoria de Compliance, Riscos e Fontes</h4>
                            <p className="text-slate-400 text-xs mt-0.5">Conformidade cadastral, pendências junto aos órgãos fiscalizadores e bases de dados auditadas.</p>
                          </div>

                          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                            
                            <div className="space-y-6">
                              {/* Dívida Ativa da União */}
                              <div className="bg-slate-950 p-5 rounded-xl border border-slate-900 space-y-4">
                                <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider border-b border-slate-900 pb-2 flex items-center gap-1.5">
                                  <ShieldAlert size={14} className="text-red-400" />
                                  Dívida Ativa da União (PGFN)
                                </h5>
                                
                                {result.divida_ativa_uniao && result.divida_ativa_uniao.length > 0 ? (
                                  <div className="space-y-3">
                                    <div className="bg-red-500/5 border border-red-500/20 p-3 rounded-lg flex items-center gap-2 text-xs text-red-400 font-bold">
                                      <AlertTriangle size={14} />
                                      Atenção: Débitos localizados inscritos na Dívida Ativa da União!
                                    </div>
                                    <div className="overflow-x-auto">
                                      <table className="w-full text-[11px] font-medium text-slate-300">
                                        <thead>
                                          <tr className="border-b border-slate-900 text-left text-slate-500 uppercase font-bold">
                                            <th className="pb-2">Inscrição</th>
                                            <th className="pb-2">Natureza</th>
                                            <th className="pb-2 text-right">Valor</th>
                                            <th className="pb-2 text-right">Situação</th>
                                          </tr>
                                        </thead>
                                        <tbody>
                                          {result.divida_ativa_uniao.map((d: any, idx: number) => (
                                            <tr key={idx} className="border-b border-slate-900/40">
                                              <td className="py-2.5 font-mono text-sky-400 font-bold">{d.inscricao}</td>
                                              <td className="py-2.5">{d.natureza || "Tributária"}</td>
                                              <td className="py-2.5 text-right font-mono text-white font-extrabold">
                                                {new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(d.valor || 0)}
                                              </td>
                                              <td className="py-2.5 text-right font-bold text-red-400">{d.situacao}</td>
                                            </tr>
                                          ))}
                                        </tbody>
                                      </table>
                                    </div>
                                  </div>
                                ) : (
                                  <div className="flex items-center gap-3 bg-emerald-500/5 border border-emerald-500/10 p-4 rounded-xl text-emerald-400 text-xs font-semibold">
                                    <CheckCircle2 size={18} className="shrink-0" />
                                    Nenhuma Dívida Ativa da União localizada junto à PGFN. Certidão Negativa de Débitos (CND) apta para emissão.
                                  </div>
                                )}
                              </div>

                              {/* Protestos em Cartórios (CENPROT) */}
                              <div className="bg-slate-950 p-5 rounded-xl border border-slate-900 space-y-4">
                                <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider border-b border-slate-900 pb-2 flex items-center gap-1.5">
                                  <AlertTriangle size={14} className="text-rose-400" />
                                  Protestos em Cartórios (CENPROT)
                                </h5>
                                
                                {(() => {
                                  const protestos = result.protestos ?? result.risk_profile?.protestos ?? [];
                                  if (protestos.length > 0) {
                                    return (
                                      <div className="space-y-3">
                                        <div className="bg-rose-500/5 border border-rose-500/20 p-3 rounded-lg flex items-center gap-2 text-xs text-rose-400 font-bold">
                                          <AlertTriangle size={14} />
                                          Atenção: Títulos protestados ativos localizados em Cartórios!
                                        </div>
                                        <div className="overflow-x-auto">
                                          <table className="w-full text-[11px] font-medium text-slate-300">
                                            <thead>
                                              <tr className="border-b border-slate-900 text-left text-slate-500 uppercase font-bold">
                                                <th className="pb-2">Cartório</th>
                                                <th className="pb-2">Documento</th>
                                                <th className="pb-2 text-right">Valor</th>
                                                <th className="pb-2 text-right">Data</th>
                                                <th className="pb-2 text-right">Status</th>
                                              </tr>
                                            </thead>
                                            <tbody>
                                              {protestos.map((p: any, idx: number) => (
                                                <tr key={idx} className="border-b border-slate-900/40">
                                                  <td className="py-2.5 font-bold text-white max-w-[150px] truncate" title={p.cartorio}>{p.cartorio}</td>
                                                  <td className="py-2.5">{p.documento_protestado}</td>
                                                  <td className="py-2.5 text-right font-mono text-white font-extrabold">
                                                    {new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(p.valor || 0)}
                                                  </td>
                                                  <td className="py-2.5 text-right font-mono">{p.data_protesto}</td>
                                                  <td className="py-2.5 text-right font-bold text-rose-400">{p.status}</td>
                                                </tr>
                                              ))}
                                            </tbody>
                                          </table>
                                        </div>
                                      </div>
                                    );
                                  } else {
                                    return (
                                      <div className="flex items-center gap-3 bg-emerald-500/5 border border-emerald-500/10 p-4 rounded-xl text-emerald-400 text-xs font-semibold">
                                        <CheckCircle2 size={18} className="shrink-0" />
                                        Nenhum protesto de títulos localizado na Central de Protesto (CENPROT).
                                      </div>
                                    );
                                  }
                                })()}
                              </div>
                            </div>

                            {/* Checklist de Requisitos */}
                            <div className="bg-slate-950 p-5 rounded-xl border border-slate-900 space-y-4">
                              <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider border-b border-slate-900 pb-2">Requisitos Mínimos Regulatórios</h5>
                              <div className="space-y-2.5">
                                <div className="flex items-center gap-2 text-xs text-emerald-400 font-medium">
                                  <CheckCircle2 size={14} />
                                  Regularidade Cadastral Ativa (CNPJ ATIVO)
                                </div>
                                <div className="flex items-center gap-2 text-xs text-emerald-400 font-medium">
                                  <CheckCircle2 size={14} />
                                  Enquadramento de Segmento Válido
                                </div>
                                <div className="flex items-center gap-2 text-xs text-emerald-400 font-medium">
                                  <CheckCircle2 size={14} />
                                  Capital Social Mínimo Atendido
                                </div>
                                <div className="flex items-center gap-2 text-xs text-emerald-400 font-medium">
                                  <CheckCircle2 size={14} />
                                  Qualificação de Representantes no QSA
                                </div>
                              </div>
                            </div>

                          </div>

                          {/* Fontes Prioritárias Consultadas */}
                          <div className="bg-slate-950 p-5 rounded-xl border border-slate-900 space-y-3">
                            <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider border-b border-slate-900 pb-2">Fontes Prioritárias de Inteligência (Sync & OSINT)</h5>
                            
                            <div className="overflow-x-auto pr-1">
                              <table className="w-full text-left text-xs text-slate-300 font-medium">
                                <thead>
                                  <tr className="border-b border-slate-900 text-slate-500 font-bold uppercase text-[10px]">
                                    <th className="pb-2">Base de Dados</th>
                                    <th className="pb-2">Nível</th>
                                    <th className="pb-2">Tipo de Dado Analisado</th>
                                    <th className="pb-2 text-right">Status do Sync</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  {result.fontes_consultadas && result.fontes_consultadas.map((f: any, idx: number) => (
                                    <tr key={idx} className="border-b border-slate-900/40 hover:bg-slate-900/20 transition-colors">
                                      <td className="py-2 font-bold text-white">{f.fonte}</td>
                                      <td className="py-2">
                                        <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded font-mono ${f.nivel === 1 ? "bg-sky-500/10 text-sky-400 border border-sky-500/20" : "bg-purple-500/10 text-purple-400 border border-purple-500/20"}`}>
                                          NÍVEL {f.nivel}
                                        </span>
                                      </td>
                                      <td className="py-2 text-slate-400">{f.tipo}</td>
                                      <td className="py-2 text-right">
                                        <span className={`text-[10px] font-bold ${f.status.includes("OK") || f.status.includes("Conectado") || f.status.includes("Sincronizado") || f.status.includes("Concluída") || f.status.includes("Ativo") ? "text-emerald-400" : "text-slate-500"}`}>
                                          ● {f.status}
                                        </span>
                                      </td>
                                    </tr>
                                  ))}
                                </tbody>
                              </table>
                            </div>
                          </div>

                        </div>
                      )}

                    </div>
                  </section>
                )}

                {/* Detail Modal Component */}
                {selectedItem && (() => {
                  const key = selectedItem.key;
                  // Normalizacao de chave: remove acentos e caracteres especiais para lookup
                  const normalizeKey = (s: string) => s?.normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[&]/g, "&");
                  const normalizedKey = normalizeKey(key);
                  const itemDetailResolved = ITEM_DETAILS[key] || Object.entries(ITEM_DETAILS).find(([k]) => normalizeKey(k) === normalizedKey)?.[1] || null;
                  const oppDetail = OPPORTUNITY_DETAILS[key] || Object.entries(OPPORTUNITY_DETAILS).find(([k]) => normalizeKey(k) === normalizedKey)?.[1] || null;
                  // Resolucao dinamica para FAPs estaduais (ex: "FAP RJ")
                  let fapDetail = null;
                  if (key && key.startsWith("FAP ")) {
                    const sc = key.substring(4).trim().toUpperCase();
                    const sf = STATE_FAP_MAP[sc];
                    const confap = ITEM_DETAILS["FAPs Estaduais"];
                    fapDetail = sf ? {
                      name: sf.name, link: sf.link,
                      description: `Auxilios estaduais para micro, pequenas e medias empresas de ${sc}.`,
                      step_by_step: [
                        `Acessar o portal da ${sf.name.split(" (")[0]} (${sf.link.replace("https://","").replace("http://","")}) e verificar editais vigentes.`,
                        "Cadastrar o proponente e a empresa na plataforma de submissao do orgao.",
                        `Elaborar o plano de trabalho e projeto de inovacao para o estado de ${sc}.`,
                        "Reunir as certidoes negativas fiscais da Uniao, Estado e Municipio e a CND do FGTS.",
                        "Submeter o edital pelo portal e acompanhar os resultados."
                      ],
                      suggested_projects: ["Projetos tecnologicos alinhados a vocacao produtiva local.", "Parcerias de P&D para digitalizacao regional."]
                    } : {
                      name: `FAP ${sc} (Fundacao de Amparo a Pesquisa)`,
                      link: confap?.link || "https://www.confap.org.br",
                      description: confap?.description || "Subvencao estadual de fomento tecnologico.",
                      step_by_step: confap?.step_by_step || ["Identificar a FAP do estado.", "Acessar o portal e verificar editais abertos."],
                      suggested_projects: confap?.suggested_projects || []
                    };
                  }

                  const itemDetail = itemDetailResolved || fapDetail || (oppDetail ? {
                    name: oppDetail.name,
                    link: "https://www.gov.br/receitafederal/pt-br",
                    description: oppDetail.estimated_potential,
                    step_by_step: oppDetail.action_plan,
                    suggested_projects: oppDetail.requirements
                  } : null);

                  const name = itemDetail?.name || selectedItem.name || selectedItem.orgao || selectedItem.tipo;
                  const link = itemDetail?.link || "https://www.gov.br/receitafederal/pt-br";
                  const description = itemDetail?.description || selectedItem.description || selectedItem.incentivo || "Detalhamento contábil e fiscal especializado.";
                  const steps = itemDetail?.step_by_step || oppDetail?.action_plan || [
                    "Acessar o portal oficial da instituição responsável pelo benefício.",
                    "Preparar e reunir as certidões negativas tributárias (CND) exigidas.",
                    "Submeter o requerimento contendo as justificativas de elegibilidade fiscal."
                  ];
                  const projects = itemDetail?.suggested_projects || (selectedItem.is_opp ? oppDetail?.requirements : null) || [
                    "Adequação e modernização de infraestrutura tecnológica da empresa.",
                    "Projetos internos de pesquisa, desenvolvimento científico e novos processos operacionais.",
                    "Aquisição e implantação de softwares licenciados com certificação produtiva."
                  ];

                  return (
                    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fadeIn">
                      <div className="bg-slate-900 border border-slate-800 w-full max-w-2xl rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
                        {/* Modal Header */}
                        <div className="bg-slate-950 p-6 border-b border-slate-800 flex items-center justify-between">
                          <div>
                            <span className="text-[9px] font-mono font-extrabold text-sky-400 uppercase tracking-widest bg-sky-950/40 px-2 py-0.5 rounded border border-sky-900/20">Detalhamento da Ação</span>
                            <h3 className="text-lg font-extrabold text-white mt-1 leading-snug">{name}</h3>
                          </div>
                          <button 
                            onClick={() => setSelectedItem(null)}
                            className="text-slate-400 hover:text-white bg-slate-800/50 hover:bg-slate-800 w-8 h-8 rounded-full flex items-center justify-center transition-colors font-bold text-sm"
                          >
                            ✕
                          </button>
                        </div>

                        {/* Modal Body */}
                        <div className="p-6 overflow-y-auto space-y-6 flex-1 text-xs">
                          {/* Description */}
                          <div className="space-y-1.5">
                            <h4 className="text-slate-400 font-bold uppercase tracking-wider text-[10px]">Benefício / Potencial Estimado</h4>
                            <p className="text-slate-200 leading-relaxed text-sm font-semibold bg-slate-950/40 p-4 rounded-xl border border-slate-850">{description}</p>
                          </div>

                          {/* Step by step */}
                          <div className="space-y-3">
                            <h4 className="text-slate-400 font-bold uppercase tracking-wider text-[10px] flex items-center gap-1.5">
                              <TrendingUp size={12} className="text-sky-400" />
                              Passo a Passo de Como Acessar / Conseguir o Edital
                            </h4>
                            <div className="space-y-3">
                              {steps.map((step, idx) => {
                                const itemKey = selectedItem.key;
                                const isCert = step.toLowerCase().includes("certid") || step.toLowerCase().includes("regularidade") || step.toLowerCase().includes("cnd");
                                const done = (checklistStates[itemKey]?.[idx] || false) || (isCert && emittedCertificates[itemKey]);
                                return (
                                  <div key={idx} className="space-y-2">
                                    <div
                                      onClick={() => setChecklistStates(prev => {
                                        const cur = [...(prev[itemKey] || [])];
                                        while (cur.length <= idx) cur.push(false);
                                        cur[idx] = !cur[idx];
                                        return { ...prev, [itemKey]: cur };
                                      })}
                                      className={`cursor-pointer border p-3 rounded-xl flex items-start gap-3 transition-all select-none ${done ? "bg-emerald-950/20 border-emerald-500/30" : "bg-slate-950 border-slate-900 hover:border-slate-700"}`}
                                    >
                                      <span className={`w-5 h-5 rounded-full text-[10px] font-bold flex items-center justify-center shrink-0 border transition-all ${done ? "bg-emerald-500/20 text-emerald-400 border-emerald-500/40" : "bg-sky-950/20 text-sky-400 border-sky-900/30"}`}>
                                        {done ? "\u2713" : idx + 1}
                                      </span>
                                      <p className={`leading-relaxed font-semibold text-xs ${done ? "line-through text-slate-500" : "text-slate-300"}`}>{step}</p>
                                    </div>
                                    {isCert && (
                                      <div className="ml-8 bg-slate-950/70 border border-slate-800 p-4 rounded-xl space-y-3" onClick={e => e.stopPropagation()}>
                                        <div className="flex items-center justify-between">
                                          <div className="flex items-center gap-2">
                                            <ShieldCheck size={14} className={emittedCertificates[itemKey] ? "text-emerald-400" : "text-sky-400"} />
                                            <span className="font-bold text-slate-200 text-xs">Emissao de Certidoes via RPA / e-CAC</span>
                                          </div>
                                          <span className={`text-[9px] font-bold px-2 py-0.5 rounded border ${emittedCertificates[itemKey] ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" : rpaRunning ? "bg-sky-500/10 text-sky-400 border-sky-500/20 animate-pulse" : "bg-slate-800/50 text-slate-400 border-slate-700"}`}>
                                            {emittedCertificates[itemKey] ? "CONCLUIDO" : rpaRunning ? `EMITINDO ${rpaProgress}%` : "DISPONIVEL"}
                                          </span>
                                        </div>
                                        <p className="text-[11px] text-slate-400">O motor preditivo automatiza a varredura no e-CAC, Policia Federal e BNMP para obter todas as certidoes exigidas.</p>
                                        {rpaRunning && (
                                          <div className="space-y-2">
                                            <div className="w-full bg-slate-900 h-1.5 rounded-full overflow-hidden">
                                              <div className="bg-sky-500 h-full transition-all duration-500" style={{ width: `${rpaProgress}%` }} />
                                            </div>
                                            <div className="bg-black/70 border border-slate-800 p-2.5 rounded-lg font-mono text-[9px] text-sky-300 max-h-28 overflow-y-auto space-y-0.5">
                                              {rpaLogs.map((log, i) => <div key={i}>{log}</div>)}
                                            </div>
                                          </div>
                                        )}
                                        {emittedCertificates[itemKey] && (
                                          <div className="grid grid-cols-2 gap-2">
                                            {["Certidao Federal RFB/PGFN","Regularidade FGTS (CRF)","Antecedentes Criminais PF","Mandados de Prisao (BNMP)"].map((cert, ci) => (
                                              <a key={ci} href="#" onClick={e => { e.preventDefault(); alert(`Download: ${cert}`); }}
                                                className="bg-slate-900 hover:bg-slate-800 p-2 rounded-lg border border-slate-700 flex items-center justify-between text-[11px] text-slate-300 hover:text-white font-semibold transition-all">
                                                <span className="truncate">{cert}</span>
                                                <Download size={11} className="text-emerald-400 shrink-0 ml-1" />
                                              </a>
                                            ))}
                                          </div>
                                        )}
                                        {!rpaRunning && !emittedCertificates[itemKey] && (
                                          <button onClick={() => runRpaSimulation(itemKey)}
                                            className="w-full bg-sky-500 hover:bg-sky-400 text-slate-950 py-2 rounded-lg text-xs font-bold transition-all flex items-center justify-center gap-1.5">
                                            <Play size={11} />
                                            Emitir Certidoes via RPA
                                          </button>
                                        )}
                                      </div>
                                    )}
                                  </div>
                                );
                              })}
                            </div>
                          </div>

                          {/* Suggested projects */}
                          {projects && projects.length > 0 && (
                            <div className="space-y-3">
                              <h4 className="text-slate-400 font-bold uppercase tracking-wider text-[10px] flex items-center gap-1.5">
                                <Brain size={12} className="text-sky-400" />
                                Projetos Elegíveis Sugeridos (Exemplos de Enquadramento)
                              </h4>
                              <div className="space-y-2">
                                {projects.map((proj, idx) => (
                                  <div key={idx} className="bg-slate-950/40 border border-slate-850 p-3 rounded-xl flex items-center gap-2.5">
                                    <span className="w-2 h-2 rounded-full bg-emerald-500 shrink-0 shadow-sm shadow-emerald-500/50" />
                                    <p className="text-slate-300 leading-relaxed font-semibold">{proj}</p>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>

                        {/* Modal Footer */}
                        <div className="bg-slate-950 p-4 border-t border-slate-800 flex items-center justify-end gap-3">
                          <button
                            onClick={() => setSelectedItem(null)}
                            className="px-4 py-2 text-xs font-bold text-slate-400 hover:text-white hover:bg-slate-900 rounded-lg transition-colors border border-slate-800"
                          >
                            Fechar
                          </button>
                          <a
                            href={link}
                            target="_blank"
                            rel="noreferrer"
                            className="bg-sky-500 hover:bg-sky-400 text-slate-950 px-4 py-2 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5 shadow-md shadow-sky-500/10 hover:scale-105 active:scale-100"
                          >
                            Acessar Portal do Edital
                            <ArrowRight size={12} />
                          </a>
                        </div>
                      </div>
                    </div>
                  );
                })()}

              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}