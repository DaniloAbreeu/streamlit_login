import streamlit as st
import streamlit_authenticator as stauth
from dependencies import consulta_nome, consulta_geral,add_registro,criar_tabela



def main():

    try:
        consulta_geral()
    except:
        criar_tabela()

    db_query= consulta_geral()

    registros = {'usernames': {}}
    for data in db_query:
        registros['usernames'][data[1]] = {'name': data[0], 'password': data[2]}


    COOKIE_EXPIRY_DAYS = 30
    authenticator = stauth.Authenticate(
        registros,
        'random_cooki_name',
        'random_signature_key',
        COOKIE_EXPIRY_DAYS,
    )

    if 'clicou_em_registrar'  not in st.session_state:
        st.session_state['clicou_em_registrar'] = False

    if st.session_state['clicou_em_registrar'] == False:
        login_form(authenticator=authenticator)
    else:
       usuario_form()


def login_form(authenticator):
    name,authentication_status,username=authenticator.login('Login')
    if authentication_status:
        authenticator.logou('Lougout', main)
        st.title('CHAT-GPT DAN')
        st.write(f'*{name} ESTÁ LOGADO!')
    elif authentication_status == False: 
        st.error('Usuario/Senha incorrentos')
    elif authentication_status == None:
        st.warning('Por favor informe um usuário e senha')
        clicou_em_registrar = st.button("Registrar")
        if clicou_em_registrar:
            st.session_state['clicou_em_registrar'] = True
            st.rerun()

def confirm_msg():
    hasher_senha=stauth.hasher([st.session_state.pswrd]).generate()
    if st.session_state.pswrd != st.session_state.confirm_pswrd:
        st.warning('Senha não conferem')
    elif consulta_nome(st.session_state.user):
        st.warning('Nome de usuário já existe')
    else:
        add_registro(st.session_state.user.nome, st.session_state.user, hasher_senha[0])
        st.success('registro efetuado!')

def usuario_form():
        with st.form(key="Formulario", clear_on_submit=True):
            nome = st.text_input("nome", key="nome")
            usurname= st.text_input("usuário", key="user")
            password=st.text_input("senha", key="pswrd",type="password")
            certo_password = st.text_input("Confirme senha", key="certo_pswrd", type="password")
            submit= st.form_submit_button(
                "salvar", on_click=confirm_msg
            )

clicou_em_fazer_login = st.button("fazer login")
if clicou_em_fazer_login:
    st.session_state['clicou_em_registrar']=False
    st.rerun()
                
if __name__ == "__main__":
    main()