# 🌲 Terê Verde Online — Plataforma Integrada de Ecoturismo (MVP)

![Logo do Projeto](nucleo/frontend/img/logo-sem-fundo-menor.png)

Plataforma digital integrada desenvolvida como MVP (Minimum Viable Product) para o curso de Tecnologia em Análise e Desenvolvimento de Sistemas. A solução centraliza informações turísticas, condições de acesso, biodiversidade e a agenda de eventos ecológicos das três principais unidades de conservação de Teresópolis, RJ, combinando um portal público interativo a um backend RESTful com persistência em banco de dados NoSQL em nuvem.

---

## 🎯 Situação-Problema

A exploração do ecoturismo na Região Serrana do Rio de Janeiro sofre historicamente com a **descentralização e assimetria de informações**. Moradores, turistas e montanhistas enfrentavam dificuldades para encontrar, em uma única fonte confiável e atualizada, dados sobre:

- Estado de abertura e conservação de trilhas e poços d'água.
- Recomendações de segurança e níveis técnicos de caminhada.
- Eventos, mutirões ecológicos e festivais da cidade.

O projeto atende diretamente as três unidades de conservação do município:

1. **Parque Nacional da Serra dos Órgãos (PARNASO)**
2. **Parque Estadual dos Três Picos (PETP)**
3. **Parque Natural Municipal Montanhas de Teresópolis (PNMMT)**

---

## 🚀 O Produto (MVP Full Stack)

A plataforma evoluiu de um front-end estático para uma **aplicação Web Full Stack completa e desacoplada**, estruturada em arquitetura cliente-servidor via API REST:

### 1. Portal Público (Experiência do Visitante)

- **Página Inicial (`index.html`):** Carrossel interativo com fotos locais em alta definição e seção de "Últimas Atualizações" alimentada diretamente pela API.
- **Catálogo de Trilhas (`trilhas.html`):** Grade de percursos com status em tempo real, altimetria, distância e **filtros dinâmicos em JavaScript** (por unidade de conservação e grau de dificuldade) sem recarregamento de página.
- **Guia de Cachoeiras (`cachoeiras.html`):** Mapeamento de quedas d'água e piscinas naturais com filtros dinâmicos por parque e avisos de balneabilidade.
- **Páginas Dedicadas aos Parques (`parque.html`, `petp.html`, `pnmt.html`):** Navegação por abas (tabs) detalhando história, normas, taxas de visitação e mapa de atrativos.
- **Agenda de Eventos (`eventos.html`):** Listagem dinâmica dos eventos cadastrados no banco de dados.

### 2. Painel Administrativo (`admin-eventos.html`)

- **Autenticação Segura:** Proteção de rotas com controle de sessão e tokens de acesso (`localStorage`).
- **CRUD Completo de Eventos:**
  - **Create:** Cadastro de novos eventos com validação de campos.
  - **Read:** Listagem em tempo real sincronizada com o MongoDB Atlas.
  - **Update:** Edição de registros existentes via requisição `PUT`.
  - **Delete:** Remoção definitiva de eventos com confirmação de segurança.

---

## 💻 Arquitetura e Tecnologias

```text
┌─────────────────────────┐         HTTP / JSON          ┌───────────────────────────┐
│     Vanilla Frontend    │  ◄────────────────────────►  │    Django REST Framework  │
│  (HTML5 / CSS3 / ES6+)  │      (Fetch API + CORS)      │       (Python 3.x API)    │
└─────────────────────────┘                              └─────────────┬─────────────┘
                                                                       │ Driver NoSQL
                                                                       ▼
                                                         ┌───────────────────────────┐
                                                         │       MongoDB Atlas       │
                                                         │     (Cluster na Nuvem)    │
                                                         └───────────────────────────┘
```
