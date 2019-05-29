from time import strftime, time, localtime
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date

db = SQLAlchemy()

TipoAtividade = {
    'minicurso': 0,
    'workshop': 1,
    'palestra': 2
}

relacao_atividade_area = db.Table('relacao_atividade_area',
                                    Column('id', Integer, primary_key=True),
                                    Column('id_atividade', Integer, db.ForeignKey('atividade.id')),
                                    Column('id_area', Integer, db.ForeignKey('area.id')))

relacao_atividade_ministrante = db.Table('relacao_atividade_ministrante',
                                         Column('id', Integer, primary_key=True),
                                         Column('id_atividade', Integer, db.ForeignKey('atividade.id')),
                                         Column('id_ministrante', Integer, db.ForeignKey('ministrante.id')))

relacao_atividade_participante = db.Table('relacao_atividade_participante',
                                          Column('id', Integer, primary_key=True),
                                          Column('id_atividade', Integer, db.ForeignKey('atividade.id')),
                                          Column('id_participante', Integer, db.ForeignKey('participante.id')))

relacao_patrocinador_evento = db.Table('relacao_patrocinador_evento',
                                       Column('id', Integer, primary_key=True),
                                       Column('id_patrocinador', Integer, db.ForeignKey('patrocinador.id')),
                                       Column('id_evento', Integer, db.ForeignKey('evento.id')))

relacao_permissao_usuario = db.Table('relacao_permissao_usuario',
                                     Column('id', Integer, primary_key=True),
                                     Column('id_usuario', Integer, db.ForeignKey('usuario.id')),
                                     Column('id_permissao', Integer, db.ForeignKey('permissao.id')))



class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    email = Column(String(64), unique=True, nullable=False)
    senha = Column(String(256), nullable=False)
    primeiro_nome = Column(String(64), nullable=False)
    sobrenome = Column(String(64), nullable=False)
    id_curso = Column(Integer, db.ForeignKey('curso.id'), nullable=True)
    id_cidade = Column(Integer, db.ForeignKey('cidade.id'), nullable=True)
    id_instituicao = Column(Integer, db.ForeignKey('instituicao.id'), nullable=True)
    token_email = Column(String(90), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    admin = Column(Boolean, default=False)
    autenticado = Column(Boolean, default=False)
    email_verificado = Column(Boolean, default=False)
    ultimo_login = Column(DateTime, default=strftime("%Y-%m-%d %H:%M:%S", localtime(time())))
    data_cadastro = Column(DateTime, default=strftime("%Y-%m-%d %H:%M:%S", localtime(time())))
    participantes_associados = db.relationship('Participante', back_populates='usuario', lazy=True)
    salt = Column(String(30), nullable=False)
    token_alteracao_senha = Column(String(90), nullable=True)
    salt_alteracao_senha = Column(String(30), nullable=True)
    permissoes_usuario = db.relationship('Permissao', secondary=relacao_permissao_usuario, lazy=True,
                                         back_populates='usuarios')
    membros_de_equipe = db.relationship('MembroDeEquipe', backref='usuario', lazy=True)
    ministrante =  db.relationship('Ministrante', back_populates='usuario', lazy=True)

    @classmethod
    def is_active(cls):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.autenticado

    @classmethod
    def is_anonymous(cls):
        return False

    def is_admin(self):
        return self.admin

    def getPermissoes(self):
        permissoes = []
        for permissao in self.permissoes_usuario:
            permissoes.append(permissao.nome)
        return permissoes

    def __repr__(self):
        return self.primeiro_nome + " " + self.sobrenome + " <" + self.email + ">"


class Participante(db.Model):
    __tablename__ = 'participante'
    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, db.ForeignKey('usuario.id'), primary_key=False)
    id_evento = Column(Integer, db.ForeignKey('evento.id'), nullable=False)
    pacote = Column(Boolean, nullable=False)
    pagamento = Column(Boolean, nullable=False)
    id_camiseta = Column(Integer, db.ForeignKey('camiseta.id'), primary_key=False)
    data_inscricao = Column(DateTime, default=strftime("%Y-%m-%d %H:%M:%S", localtime(time())))
    credenciado = Column(Boolean, nullable=False)
    opcao_coffee = Column(Integer, nullable=False)
    usuario = db.relationship('Usuario', back_populates='participantes_associados', lazy=True)
    presencas = db.relationship('Presenca', backref='participante')
    atividades = db.relationship('Atividade', secondary=relacao_atividade_participante, lazy=True,
                                 back_populates='participantes')

    def __repr__(self):
        return self.usuario.primeiro_nome + " " + self.usuario.sobrenome + " <" + self.email + ">"


class Ministrante(db.Model):
    __tablename__ = 'ministrante'
    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, db.ForeignKey('usuario.id'))
    telefone = Column(String(11), nullable=False)
    profissao = Column(String(64), nullable=False)
    empresa_universidade = Column(String(64))
    biografia = Column(String(1500), nullable=False)
    foto = Column(String(128))
    tamanho_camiseta = Column(Integer)
    facebook = Column(String(64))
    twitter = Column(String(64))
    linkedin = Column(String(64))
    github = Column(String(64))
    atividades = db.relationship('Atividade', secondary=relacao_atividade_ministrante, lazy=True,
                                back_populates='ministrantes')
    usuario =  db.relationship('Usuario', back_populates='ministrante', lazy=True)

    def __repr__(self):
        return self.usuario.nome

class DadosHospedagemTransporte(db.Model):
    __tablename__ = 'dados_hospedagem_transporte'
    id = Column(Integer, primary_key=True)
    id_ministrante = Column(Integer, db.ForeignKey('ministrante.id'))
    id_evento = Column(Integer, db.ForeignKey('evento.id'))
    cidade_origem = Column(String(64), nullable=False)
    data_chegada_origem = Column(Date, nullable=False)
    data_chegada_partida = Column(Date, nullable=False)
    transporte_ida_volta = Column(Boolean, nullable=False)
    opcoes_transporte_ida_volta = Column(Integer)
    transporte_sanca = Column(Boolean, nullable=False)
    opcoes_transporte_sanca = Column(Integer)
    hospedagem = Column(Boolean, nullable=False)
    necessidades_hospedagem = Column(String(256))
    observacoes = Column(String(256))


class AreaAtividade(db.Model):
    __tablename__ = 'area'
    id = Column(Integer, primary_key=True)
    nome = Column(String(24), nullable=False)


class Atividade(db.Model):
    __tablename__ = 'atividade'
    id = Column(Integer, primary_key=True)
    id_ministrante = Column(Integer, db.ForeignKey('ministrante.id'))
    id_evento = Column(Integer, db.ForeignKey('evento.id'))
    vagas_totais = Column(Integer, nullable=False)
    vagas_disponiveis = Column(Integer, nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)
    tipo = Column(Integer, nullable=False)
    data_hora = Column(DateTime, nullable=False)
    local = Column(String(64), nullable=False)
    titulo = Column(String(64), nullable=False)
    descricao = Column(String(1024), nullable=False)
    observacoes = Column(String(512), nullable=False)
    ministrantes = db.relationship('Ministrante', secondary=relacao_atividade_ministrante, lazy=True,
                                   back_populates='atividades')
    participantes = db.relationship('Participante', secondary=relacao_atividade_participante, lazy=True,
                                    back_populates='atividades')
    presencas = db.relationship('Presenca', backref='atividade')

    def __repr__(self):
        return self.titulo


class Minicurso(db.Model):
    __tablename__ = 'minicurso'
    id = Column(Integer, primary_key=True)
    pre_requisitos = Column(String(128))
    planejamento = Column(String(128))
    apresentacao_extra = Column(String(128))
    material = Column(String(128))
    requisitos_hardware = Column(String(1024))
    requisitos_software = Column(String(1024))
    dicas_instalacao = Column(String(1024))
    observacoes = Column(String(1024))

class Palestra(db.Model):
    __tablename__ = 'palestra'
    id = Column(Integer, primary_key=True)
    planejamento = Column(String(128))
    apresentacao_extra = Column(String(128))
    material = Column(String(128))
    requisitos_tecnicos = Column(String(1024))
    observacoes = Column(String(1024))

class FeiraDePesquisas(db.Model):
    id = Column(Integer, primary_key=True)
    necessidades = Column(String(1024))
    planejamento = Column(String(1024))

class Evento(db.Model):
    __tablename__ = 'evento'
    id = Column(Integer, primary_key=True)
    edicao = Column(Integer, nullable=False)
    data_hora_inicio = Column(DateTime, nullable=False)
    data_hora_fim = Column(DateTime, nullable=False)
    inicio_inscricoes_evento = Column(DateTime, nullable=False)
    fim_inscricoes_evento = Column(DateTime, nullable=False)
    ano = Column(Integer, default=datetime.now().year)
    participantes = db.relationship('Participante', backref='evento', lazy=True)
    presencas = db.relationship('Presenca', backref='evento', lazy=True)
    atividades = db.relationship('Atividade', backref='evento', lazy=True)
    membros_equipe = db.relationship('MembroDeEquipe', backref='evento', lazy=True)
    patrocinadores = db.relationship('Patrocinador', secondary=relacao_patrocinador_evento, lazy=True,
                                     back_populates='eventos')
    camisetas = db.relationship('Camiseta', backref='evento', lazy=True)

    def __repr__(self):
        return str(self.edicao) + "ª Edição"


class Presenca(db.Model):
    __tablename__ = 'presenca'
    id = Column(Integer, primary_key=True)
    data_hora_registro = Column(DateTime, nullable=False)
    id_atividade = Column(Integer, db.ForeignKey('atividade.id'), nullable=False)
    id_participante = Column(Integer, db.ForeignKey('participante.id'), nullable=False)
    id_evento = Column(Integer, db.ForeignKey('evento.id'), nullable=False)
    inscrito = Column(Boolean, nullable=False)


class MembroDeEquipe(db.Model):
    __tablename__ = 'membro_de_equipe'
    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, db.ForeignKey('usuario.id'), nullable=False)
    foto = Column(String(100), nullable=True)
    email_secomp = Column(String(254), nullable=True)
    id_cargo = Column(Integer, db.ForeignKey('cargo.id'), nullable=False)
    id_diretoria = Column(Integer, db.ForeignKey('diretoria.id'), nullable=False)
    id_evento = Column(Integer, db.ForeignKey('evento.id'), nullable=False)

    def __repr__(self):
        return self.usuario.primeiro_nome + " " + self.usuario.sobrenome + "<" + self.usuario.email + ">"


class Cargo(db.Model):
    __tablename__ = 'cargo'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    membros = db.relationship('MembroDeEquipe', backref='cargo', lazy=True)

    def __repr__(self):
        return self.nome


class Diretoria(db.Model):
    __tablename__ = 'diretoria'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    ordem = Column(Integer, nullable=False)
    membros = db.relationship('MembroDeEquipe', backref='diretoria', lazy=True)

    def __repr__(self):
        return self.nome


class Patrocinador(db.Model):
    __tablename__ = 'patrocinador'
    id = Column(Integer, primary_key=True)
    nome_empresa = Column(String(100), nullable=False)
    logo = Column(String(100), nullable=False)
    ativo_site = Column(Boolean, nullable=False)
    id_cota = Column(Integer, db.ForeignKey('cota_patrocinio.id'), nullable=False)
    ordem_site = Column(Integer, primary_key=True)
    link_website = Column(String(200), nullable=True)
    ultima_atualizacao_em = Column(DateTime, default=strftime("%Y-%m-%d %H:%M:%S", localtime(time())))
    eventos = db.relationship('Evento', secondary=relacao_patrocinador_evento, lazy=True,
                              back_populates='patrocinadores')

    def __repr__(self):
        return self.nome_empresa


class CotaPatrocinio(db.Model):
    __tablename__ = 'cota_patrocinio'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    patrocinadores = db.relationship('Patrocinador', backref='cota_patrocinio', lazy=True)


class Curso(db.Model):
    __tablename__ = 'curso'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    usuarios = db.relationship('Usuario', backref='curso', lazy=True)

    def __repr__(self):
        return self.nome


class Instituicao(db.Model):
    __tablename__ = 'instituicao'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    usuarios = db.relationship('Usuario', backref='instituicao', lazy=True)

    def __repr__(self):
        return self.nome


class Cidade(db.Model):
    __tablename__ = 'cidade'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    usuarios = db.relationship('Usuario', backref='cidade', lazy=True)

    def __repr__(self):
        return self.nome


class Camiseta(db.Model):
    __tablename__ = 'camiseta'
    id = Column(Integer, primary_key=True)
    id_evento = Column(Integer, db.ForeignKey('evento.id'), nullable=False)
    participantes = db.relationship('Participante', backref='camiseta', lazy=True)
    tamanho = Column(String(30), nullable=False)
    quantidade = Column(Integer, nullable=False)
    ordem_site = Column(Integer, nullable=False)
    quantidade_restante = Column(Integer, nullable=False)

    def __repr__(self):
        return self.nome


class Permissao(db.Model):
    __tablename__ = 'permissao'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    usuarios = db.relationship('Usuario', secondary=relacao_permissao_usuario, lazy=True,
                               back_populates='permissoes_usuario')

    def __repr__(self):
        return self.nome

class URLConteudo(db.Model):
    __tablename__ = 'urlconteudo'
    id = Column(Integer, primary_key=True)
    descricao = Column(String(100), nullable=False)
    codigo = Column(String(200), nullable=False)
    ultimo_gerado = Column(Boolean, default=False, nullable=False)
    valido = Column(Boolean, default=True, nullable=False)
    numero_cadastros = Column(Integer, default=1)
