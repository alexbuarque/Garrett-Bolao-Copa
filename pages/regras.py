import streamlit as st

st.title("🏅 Prêmios e Regras")

# ── Regras ────────────────────────────────────────────────────────────────────
st.header("📋 Regras de Pontuação")

st.markdown(
    """
    <table style="width:100%;border-collapse:collapse;margin-bottom:1rem">
        <thead>
            <tr style="background-color:#2e7d32;color:white">
                <th style="padding:12px 16px;text-align:left;border:1px solid #ccc">Tipo de Acerto</th>
                <th style="padding:12px 16px;text-align:center;border:1px solid #ccc">Pontos</th>
            </tr>
        </thead>
        <tbody>
            <tr style="background-color:#1e1e1e;color:#ffffff">
                <td style="padding:12px 16px;border:1px solid #555">Placar Exato</td>
                <td style="padding:12px 16px;text-align:center;border:1px solid #555"><b>5</b></td>
            </tr>
            <tr style="background-color:#2a2a2a;color:#ffffff">
                <td style="padding:12px 16px;border:1px solid #555">Resultado Correto</td>
                <td style="padding:12px 16px;text-align:center;border:1px solid #555"><b>3</b></td>
            </tr>
            <tr style="background-color:#1e1e1e;color:#ffffff">
                <td style="padding:12px 16px;border:1px solid #555">Erro</td>
                <td style="padding:12px 16px;text-align:center;border:1px solid #555"><b>0</b></td>
            </tr>
        </tbody>
    </table>
    """,
    unsafe_allow_html=True,
)

st.markdown("#### Como funciona o acerto?")
st.markdown("A pontuação é definida conforme o nível de acerto do palpite:")
st.markdown(
    "**Placar exato:** quando você acerta a quantidade de gols de cada time na partida."
)
st.markdown(
    "**Resultado correto:** quando você acerta o vencedor da partida ou o empate, "
    "independentemente do número de gols."
)
st.info(
    "Os pontos **não são acumulativos**. Ou seja, ao acertar o placar exato, você recebe "
    "apenas a pontuação máxima desse acerto, não sendo somada a pontuação de resultado correto.",
    icon="ℹ️",
)
