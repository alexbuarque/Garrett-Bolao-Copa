# Bolão da Copa 2026 ⚽

Aplicativo de bolão para a Copa do Mundo 2026, construído com **Streamlit** e **Supabase**.

## Funcionalidades

- 🔐 Cadastro e login com email/senha (Supabase Auth)
- ⚽ Palpites para todos os 72 jogos da fase de grupos (12 grupos × 6 jogos)
- 🌟 Palpites especiais: Artilheiro, MVP e Melhor Goleiro (10 pts cada)
- 🏆 Ranking em tempo real com breakdown de pontos
- 🔧 Painel admin para inserir resultados e recalcular pontos automaticamente

## Sistema de Pontuação

| Acerto | Pontos |
|--------|--------|
| Placar exato | **5 pts** |
| Vencedor/empate (placar errado) | **3 pts** |
| Gols de um time corretos (sem placar exato) | **+1 pt por time** |
| Artilheiro correto | **10 pts** |
| MVP correto | **10 pts** |
| Melhor Goleiro correto | **10 pts** |
