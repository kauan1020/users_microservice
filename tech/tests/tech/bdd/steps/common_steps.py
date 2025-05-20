from behave import then
import re

@then('the common error message should contain "{expected_text}"')
def step_impl(context, expected_text):
    """
    Verifica se a mensagem de erro contém o texto esperado.
    Este passo pode ser usado por qualquer feature quando houver necessidade
    de verificar mensagens de erro.
    """
    assert context.error is not None
    assert expected_text in context.error