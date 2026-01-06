# Parque Aquático

**Leia** [o guia](https://github.com/mate-academy/py-task-guideline/blob/main/README.md) antes de começar.

Você é um visitante de um parque aquático. Existem vários toboáguas com diferentes limitações de altura, peso e idade. 
Vamos criar um sistema que determina se um visitante pode usar o toboágua dependendo de seus próprios parâmetros.

Para implementá-lo, crie as seguintes classes:

#### 1. Classe `IntegerRange` - descritor para limitações de parâmetros
Seu método `__init__` recebe 2 valores e os armazena:
   - `min_amount` - valor inteiro mínimo acessível do parâmetro do visitante
   - `max_amount` - valor inteiro máximo acessível do parâmetro do visitante

Crie os métodos `__get__()`, `__set__()` e `__set_name__()`.
O método `__set__()` precisa ter uma lógica para validar que o valor está entre `min_amount` e `max_amount` e será usado nas classes Validadoras.
Não se esqueça de verificar o tipo do valor antes de defini-lo. Você pode lançar TypeError ou ValueError
durante a validação. As mensagens de erro podem ser omitidas.


#### 2. Classe `Visitor` que é responsável pelos dados pessoais do usuário
Seu método `__init__` recebe `name`, `age`, `weight` e `height`. `Visitor` não tem nenhuma limitação.


#### 3. Classe `SlideLimitationValidator`
Seu método `__init__` recebe `age`, `weight` e `height`. Nenhum método adicional é necessário aqui.
Esta é uma classe base para Validadores, portanto nenhuma validação é necessária.


#### 4. Classes `ChildrenSlideLimitationValidator` e `AdultSlideLimitationValidator`, são validadores de limitação para toboáguas
O parque aquático tem dois tipos de toboáguas: para adultos e para crianças.

Classe `ChildrenSlideLimitationValidator` e defina os valores:
   - `age` no intervalo de `4` a `14`
   - `height` no intervalo de `80` a `120`
   - `weight` no intervalo de `20` a `50`

Classe `AdultSlideLimitationValidator` e defina os valores:
   - `age` no intervalo de `14` a `60`
   - `height` no intervalo de `120` a `220`
   - `weight` no intervalo de `50` a `120`

Essas classes devem herdar de `SlideLimitationValidator`. Nenhum método adicional é necessário aqui.

#### 5. Classe `Slide`
Seu método `__init__` recebe 2 argumentos:
   - `name` - valor string, nome do toboágua
   - `limitation_class` - uma das classes filhas de `SlideLimitationValidator` que define restrições sobre o uso do Toboágua.
   Observe que o construtor deve armazenar apenas a classe em si e não instanciar uma instância dela.

Crie um método chamado `can_access` que verifica se um Visitante pode usar o toboágua, retornando True ou False.
Para validar os atributos do Visitante, crie uma instância de `limitation_class`. Você não precisa armazenar essa instância em lugar nenhum.
O método `can_access` deve lidar com todos os possíveis erros que podem ser lançados pela `limitation_class`.

### Observação: Verifique seu código usando esta [checklist](checklist.md) antes de enviar sua solução.
