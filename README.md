<!-- Banner SVG animado -->
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:fc00ff,100:00dbde&height=180&section=header&text=Alyson%20Trizotto&fontSize=40&fontAlign=50&fontColor=fff"/>
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=24&pause=1000&color=00DBDE&center=true&vCenter=true&width=600&lines=Desenvolvedor+Back-end;Especialista+em+APIs+e+Microservi%C3%A7os;Apaixonado+por+inova%C3%A7%C3%A3o+e+tecnologia"/>
</p>

---

## 👨‍💻 Sobre mim
Sou Desenvolvedor com sólida experiência em back-end, especialista em PHP, Laravel e bancos de dados relacionais. Tenho profundo conhecimento em construção de APIs REST, microserviços, testes unitários e integração contínua com Git e Docker. Atuo desde a arquitetura até a implantação, sempre buscando inovação e excelência técnica.

Experiência avançada no consumo de APIs bancárias (Banco do Brasil, Mercado Pago) e processamento massivo de pagamentos, incluindo automação de geração e liquidação de boletos bancários. Atuação em projetos de telemetria veicular, integração com atuadores e sistemas embarcados para monitoramento e controle remoto de frotas.

Forte domínio em arquitetura de sistemas escaláveis, integração de serviços, mensageria, observabilidade, pipelines CI/CD e persistência em cloud.

---

## 🚀 Principais Skills
<p align="center">
  <img src="https://skillicons.dev/icons?i=php,laravel,nodejs,js,ts,docker,git,github,bash,linux,aws,azure,gcp,postgres,mysql,oracle,redis,graphql,nginx,vercel,socketio,githubactions"/>
</p>

- Hooks e eventos (Laravel, Node.js)
- Gateways de pagamento e APIs externas
- Sockets e comunicação em tempo real
- Notificações (e-mail, push, SMS, WhatsApp)
- Persistência em cloud (AWS, Azure, GCP)
- Pipelines e esteira de CI/CD
- Testes automatizados e integração contínua

---

## 🏆 Destaques Profissionais
- Desenvolvimento e manutenção de microserviços robustos (omnichannel, serviços bancários, autenticação)
- Construção de back-end omnichannel integrando WhatsApp, e-mail, mobile, web e automações internas
- Construção de aplicação bancária
- Desenvolvimento de IA para reconhecimento de placas veiculares e caracteres
- Participação ativa em todas as etapas do ciclo de desenvolvimento
- Experiência em treinamento, mentoring e liderança técnica de equipes

---

## 💡 Pontos Fortes
- Versatilidade: domínio de múltiplas tecnologias e linguagens
- Proatividade: busca constante por inovação e aprimoramento
- Trabalho em equipe: colaboração com diferentes áreas e perfis
- Liderança técnica: capacitação e mentoring de desenvolvedores

---

## 📊 Estatísticas do GitHub
<!-- <p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=AlysonTrizotto&show_icons=true&theme=radical"/>
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=AlysonTrizotto&layout=compact&theme=radical"/>
</p> -->
<p align="center">
  <img src="./stats.svg"/>
  <img src="./langs.svg"/>
</p>



## 🚀 Biblioteca em Desenvolvimento: laravel-ddl-crud

O [laravel-ddl-crud](https://github.com/AlysonTrizotto/laravel-ddl-crud) é uma biblioteca para Laravel que permite criar, alterar e excluir tabelas e campos do banco de dados via código, além de gerar automaticamente rotas, controllers e views para operações CRUD. Ideal para aplicações que precisam de flexibilidade na estrutura dos dados em tempo de execução.

**Principais recursos:**
- Criação dinâmica de tabelas e campos usando DDL (Data Definition Language).
- Geração automática de CRUD completo (rotas, controllers, views) a partir das definições das tabelas.
- Manipulação de esquemas de banco de dados sem necessidade de migrações manuais.
- Testes automatizados com PHPUnit para garantir a integridade das operações.

**Exemplo de uso:**
```sql

CREATE TABLE customers (
    id         BIGSERIAL PRIMARY KEY,
    name       VARCHAR(255)  NOT NULL,
    email      CITEXT        NOT NULL UNIQUE,
    created_at TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ   NULL,
    UNIQUE (email)
);

CREATE INDEX idx_customers_email ON customers (email);

CREATE TABLE customer_favorites (
    id          BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    product_id  BIGINT NOT NULL, -- ID externo do produto (FakeStore)
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at  TIMESTAMPTZ NULL,
    UNIQUE (customer_id, product_id)
);

CREATE INDEX idx_customer_favorites_customer ON customer_favorites (customer_id);
CREATE INDEX idx_customer_favorites_product  ON customer_favorites (product_id);

create table users (
    id int primary key auto_increment,
    name varchar(255) not null,
    email varchar(255) not null unique,
    password varchar(255) not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    deleted_at timestamp default null on delete current_timestamp
);

create index idx_email_password on users (email, password);


```

**Tecnologias utilizadas:**
- Laravel 12+
- PHP 8.2+
- PHPUnit

**Status:** Em desenvolvimento ativo.  
**Colabore:** Sugestões, issues e pull requests são bem-vindos!

Mais detalhes e documentação completa no repositório:  
👉 [github.com/AlysonTrizotto/laravel-ddl-crud](https://github.com/AlysonTrizotto/laravel-ddl-crud)


## 📫 Contato
<p align="center">
  <a href="https://www.linkedin.com/in/alyson-trizotto" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/>
  </a>
  <a href="https://wa.me/+5541988264079?text=Ol%C3%A1%2C%20gostaria%20de%20entrar%20em%20contato!" target="_blank">
    <img src="https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white"/>
  </a>
  <a href="https://alysontrizotto.vercel.app" target="_blank">
    <img src="https://img.shields.io/badge/Meu%20Site-000?style=for-the-badge&logo=vercel&logoColor=white"/>
  </a>
</p>

---

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:fc00ff,100:00dbde&height=100&section=footer"/>
</p>

