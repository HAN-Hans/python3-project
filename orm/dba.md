[对象关系教程](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#object-relational-tutorial)

SQLAlchemy对象关系映射器提供了一种方法，用于将用户定义的Python类与数据库表相关联，并将这些类（对象）的实例与其对应表中的行相关联。它包括一个透明地同步对象及其相关行之间状态的所有变化的系统，称为[工作单元](http://docs.sqlalchemy.org/en/latest/glossary.html#term-unit-of-work)，以及根据用户定义的类及其定义的彼此之间的关系表达数据库查询的系统。

ORM与构建ORM的SQLAlchemy表达式语言形成对比。在[SQL表达式语言教程中](http://docs.sqlalchemy.org/en/latest/core/tutorial.html)引入的 [SQL表达式语言](http://docs.sqlalchemy.org/en/latest/core/tutorial.html)提出了一种直接表示关系数据库的原始结构而没有意见的系统，而ORM提供了一种高级和抽象的使用模式，它本身就是应用的一个例子。表达语言。

虽然ORM和表达语言的使用模式之间存在重叠，但相似之处比最初出现时更为肤浅。从用户定义的[域模型](http://docs.sqlalchemy.org/en/latest/glossary.html#term-domain-model)的角度来看，数据的结构和内容是从其底层存储模型透明地持久化和刷新的。另一个从文字模式和SQL表达式表示的角度来看它，它们明确地组成由数据库单独使用的消息。

可以使用Object Relational Mapper专门构建成功的应用程序。在高级情况下，使用ORM构建的应用程序可能会在需要特定数据库交互的某些区域中直接使用表达式语言。

## Connecting

在本教程中，我们将使用仅内存的SQLite数据库。要连接我们使用[`create_engine()`](http://docs.sqlalchemy.org/en/latest/core/engines.html)：

![create_engine](http://upload-images.jianshu.io/upload_images/13148580-2e37e63eafa97654.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```python
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine('mysql+mysqldb://scott:tiger@localhost/foo')

def connect():
    return psycopg.connect(user='scott', host='localhost')

create_engine(
    case_sensitive=True,  # 大小写敏感
    connect_args={'argument1':17, 'argument2':'bar'},  # 直接传递到DBAPI的选项字典connect()方法
    convert_unicode=False,  # 自动将String转成unicode
    creator=connect,  # 一个可调用的返回一个DBAPI连接。此创建函数将传递给基础连接池，并将用于创建所有新的数据库连接。使用此函数会导致绕过URL参数中指定的连接参数。
    echo=False,  # True，Engine会将所有语句及其参数列表的repr()记录到引擎记录器，默认为sys.stdout
    echo_pool=False  # 如果为True，连接池将记录所有输入/输出到日志流
    empty_in_strategy='static',  # 为右侧是空集的位置呈现`IN`或`NOT IN`表达式时使用的SQL编译策略
    encoding='utf-8',  # 用于字符串编码/解码操作的字符串编码
    execution_options={},  # 
```

该`echo`标志是设置SQLAlchemy日志记录的快捷方式，可通过Python的标准`logging`模块完成。启用它后，我们将看到生成的所有生成的SQL。如果您正在完成本教程并希望生成更少的输出，请将其设置为`False`。本教程将在弹出窗口后面格式化SQL，这样就不会妨碍我们; 只需单击“SQL”链接即可查看正在生成的内容。

返回值[`create_engine()`](http://docs.sqlalchemy.org/en/latest/core/engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")是一个实例 [`Engine`](http://docs.sqlalchemy.org/en/latest/core/connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")，它代表数据库的核心接口，通过一个方言进行调整，该方言处理数据库和[正在](http://docs.sqlalchemy.org/en/latest/glossary.html#term-dbapi)使用的[DBAPI](http://docs.sqlalchemy.org/en/latest/glossary.html#term-dbapi)的细节。在这种情况下，SQLite方言将解释Python内置`sqlite3` 模块的指令。

懒惰连接

的[`Engine`](http://docs.sqlalchemy.org/en/latest/core/connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")，当第一次返回的[`create_engine()`](http://docs.sqlalchemy.org/en/latest/core/engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")，其实并没有试图连接到数据库之中; 只有在第一次要求它对数据库执行任务时才会发生这种情况。

第一次 调用[`Engine.execute()`](http://docs.sqlalchemy.org/en/latest/core/connections.html#sqlalchemy.engine.Engine.execute "sqlalchemy.engine.Engine.execute")或[`Engine.connect()`](http://docs.sqlalchemy.org/en/latest/core/connections.html#sqlalchemy.engine.Engine.connect "sqlalchemy.engine.Engine.connect")调用方法时，[`Engine`](http://docs.sqlalchemy.org/en/latest/core/connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")建立与数据库的真实[DBAPI](http://docs.sqlalchemy.org/en/latest/glossary.html#term-dbapi)连接，然后用于发出SQL。使用ORM时，我们通常不会在[`Engine`](http://docs.sqlalchemy.org/en/latest/core/connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")创建后直接使用; 相反，它将在ORM的幕后使用，我们很快就会看到。

也可以看看

[数据库URL](http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls) - 包括[`create_engine()`](http://docs.sqlalchemy.org/en/latest/core/engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine") 连接到多种数据库的示例，其中包含指向更多信息的链接。

## 声明映射

使用ORM时，配置过程首先描述我们将要处理的数据库表，然后定义我们自己的类，这些类将映射到这些表。在现代SQLAlchemy中，这两个任务通常使用称为[Declarative](http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/index.html)的系统一起执行，这允许我们创建包含指令的类，以描述它们将映射到的实际数据库表。

使用Declarative系统映射的类是根据基类定义的，该基类维护相对于该基类的类和表的目录 - 这称为**声明性基类**。我们的应用程序通常在一个常用的模块中只有一个这个基础的实例。我们使用[`declarative_base()`](http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/api.html#sqlalchemy.ext.declarative.declarative_base "sqlalchemy.ext.declarative.declarative_base") 函数创建基类，如下所示：

```python
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
```

现在我们有了一个“基础”，我们可以根据它定义任意数量的映射类。我们将从一个名为的表开始`users`，它将使用我们的应用程序为最终用户存储记录。调用的新类`User`将是我们映射此表的类。在类中，我们定义了有关我们将要映射的表的详细信息，主要是表名，以及列的名称和数据类型：

使用Declarative的类至少需要一个`__tablename__`属性，并且至少有一个 [`Column`](http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")属于主键的一部分。SQLAlchemy从不对类引用的表做任何假设，包括它没有名称，数据类型或约束的内置约定。但这并不意味着需要样板; 相反，我们鼓励您使用辅助函数和mixin类创建自己的自动约定，这在[Mixin和Custom Base Classes](http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/mixins.html#declarative-mixins)中有详细描述。

构造我们的类时，Declarative将所有[`Column`](http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column") 对象替换为称为[描述符的](http://docs.sqlalchemy.org/en/latest/glossary.html#term-descriptors)特殊Python访问器; 这是一个称为[仪器](http://docs.sqlalchemy.org/en/latest/glossary.html#term-instrumentation)的过程。“instrumented”映射类将为我们提供在SQL上下文中引用表的方法，以及从数据库中持久保存和加载列的值。

除了映射过程对我们的类所做的之外，该类仍然主要是一个普通的Python类，我们可以定义我们的应用程序所需的任意数量的普通属性和方法。

有关为何需要主键的信息，请参阅 [如何映射没有主键的表？](http://docs.sqlalchemy.org/en/latest/faq/ormconfiguration.html#faq-mapper-primary-key)。 

## 创建架构

`User`通过声明系统构建我们的类，我们定义了有关表的信息，称为表元数据。SQLAlchemy用于表示特定表的此信息的[`Table`](http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象称为对象，这里Declarative为我们创建了一个对象。我们可以通过检查`__table__`属性来看到这个对象：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> User.__table__ 
Table('users', MetaData(bind=None),
 Column('id', Integer(), table=<users>, primary_key=True, nullable=False),
 Column('name', String(), table=<users>),
 Column('fullname', String(), table=<users>),
 Column('password', String(), table=<users>), schema=None)</pre>

古典映射

虽然强烈建议使用Declarative系统，但不需要使用SQLAlchemy的ORM。在Declarative之外，任何普通的Python类都可以直接映射到[`Table`](http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table") 使用该[`mapper()`](http://docs.sqlalchemy.org/en/latest/orm/mapping_api.html#sqlalchemy.orm.mapper "sqlalchemy.orm.mapper")函数的任何类; 这种不太常见的用法在[Classical Mappings中](http://docs.sqlalchemy.org/en/latest/orm/mapping_styles.html#classical-mapping)有所描述。

当我们声明我们的类时，Declarative使用Python元类，以便在类声明完成后执行其他活动; 在此阶段，它[`Table`](http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")根据我们的规范创建了一个对象，并通过构造一个[`Mapper`](http://docs.sqlalchemy.org/en/latest/orm/mapping_api.html#sqlalchemy.orm.mapper.Mapper "sqlalchemy.orm.mapper.Mapper")对象将其与类相关联。这个对象是我们通常不需要直接处理的幕后对象（尽管它可以在我们需要时提供有关我们的映射的大量信息）。

该[`Table`](http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")对象是一个更大的集合的成员，称为[`MetaData`](http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData")。使用Declarative时，可以使用`.metadata` 声明性基类的属性来使用此对象。

这[`MetaData`](http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData") 是一个注册表，包括向数据库发出一组有限的模式生成命令的功能。由于我们的SQLite数据库实际上没有`users`表，我们可以使用[`MetaData`](http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.MetaData "sqlalchemy.schema.MetaData") 为所有尚不存在的表向数据库发出CREATE TABLE语句。下面，我们调用该[`MetaData.create_all()`](http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.MetaData.create_all "sqlalchemy.schema.MetaData.create_all")方法，将我们[`Engine`](http://docs.sqlalchemy.org/en/latest/core/connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine") 作为数据库连接源传递。我们将看到首先发出特殊命令以检查`users`表的存在，然后是实际的语句：`CREATE TABLE`

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> Base.metadata.create_all(engine)
SELECT ...
PRAGMA table_info("users")
()
CREATE TABLE users (
    id INTEGER NOT NULL, name VARCHAR,
    fullname VARCHAR,
    password VARCHAR,
    PRIMARY KEY (id)
)
()
COMMIT</pre>

最小表格描述与完整描述

熟悉CREATE TABLE语法的用户可能会注意到VARCHAR列的生成没有长度; 在SQLite和PostgreSQL上，这是一种有效的数据类型，但在其他情况下，它是不允许的。因此，如果在其中一个数据库上运行本教程，并且您希望使用SQLAlchemy发出CREATE TABLE，则可以向该[`String`](http://docs.sqlalchemy.org/en/latest/core/type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")类型提供“length” ，如下所示：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">Column(String(50))</pre>

在长度字段[`String`](http://docs.sqlalchemy.org/en/latest/core/type_basics.html#sqlalchemy.types.String "sqlalchemy.types.String")，以及关于可用类似精度/规模字段[`Integer`](http://docs.sqlalchemy.org/en/latest/core/type_basics.html#sqlalchemy.types.Integer "sqlalchemy.types.Integer")，[`Numeric`](http://docs.sqlalchemy.org/en/latest/core/type_basics.html#sqlalchemy.types.Numeric "sqlalchemy.types.Numeric")等不会被其他的SQLAlchemy创建表时比引用。

此外，Firebird和Oracle需要序列来生成新的主键标识符，而SQLAlchemy不会在未经指示的情况下生成或假设这些标识符。为此，您使用[`Sequence`](http://docs.sqlalchemy.org/en/latest/core/defaults.html#sqlalchemy.schema.Sequence "sqlalchemy.schema.Sequence")构造：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">from sqlalchemy import Sequence
Column(Integer, Sequence('user_id_seq'), primary_key=True)</pre>

[`Table`](http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")因此，通过我们的声明性映射生成的完整，万无一失的因素是：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
                                self.name, self.fullname, self.password)</pre>

我们分别包含这个更详细的表定义，以突出主要针对Python内使用的最小构造与将用于在具有更严格要求的特定后端集上发出CREATE TABLE语句之间的区别。

## 创建映射类的实例[](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#create-an-instance-of-the-mapped-class "永久链接到这个标题")

完成映射后，现在让我们创建并检查一个`User`对象：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
>>> ed_user.name
'ed'
>>> ed_user.password
'edspassword'
>>> str(ed_user.id)
'None'</pre>

该`__init__()`方法

我们的`User`类（使用Declarative系统定义）提供了一个构造函数（例如`__init__()`方法），它自动接受与我们映射的列匹配的关键字名称。我们可以自由地`__init__()`在我们的类上定义我们喜欢的任何显式方法，它将覆盖Declarative提供的默认方法。

尽管我们没有在构造函数中指定它，但是当我们访问它时，该`id`属性仍会产生一个值`None`（而不是Python通常的提升`AttributeError`未定义属性的行为）。SQLAlchemy的[检测](http://docs.sqlalchemy.org/en/latest/glossary.html#term-instrumentation)通常在首次访问时为列映射属性生成此默认值。对于我们实际分配了值的那些属性，检测系统正在跟踪这些分配，以便在最终的INSERT语句中使用以发送到数据库。

## 创建会话[](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#creating-a-session "永久链接到这个标题")

我们现在准备开始与数据库交谈了。ORM对数据库的“处理”是[`Session`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。当我们第一次设置应用程序时，在与[`create_engine()`](http://docs.sqlalchemy.org/en/latest/core/engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine") 语句相同的级别上，我们定义一个[`Session`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")类，它将作为新[`Session`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session") 对象的工厂：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> from sqlalchemy.orm import sessionmaker
>>> Session = sessionmaker(bind=engine)</pre>

如果您的应用程序尚未 [`Engine`](http://docs.sqlalchemy.org/en/latest/core/connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")定义模块级对象，请将其设置为：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> Session = sessionmaker()</pre>

稍后，当您使用创建引擎时[`create_engine()`](http://docs.sqlalchemy.org/en/latest/core/engines.html#sqlalchemy.create_engine "sqlalchemy.create_engine")，将其连接到[`Session`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")使用 [`configure()`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.sessionmaker.configure "sqlalchemy.orm.session.sessionmaker.configure")：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> Session.configure(bind=engine)  # once engine is available</pre>

会话生命周期模式

何时制作a的问题在[`Session`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")很大程度上取决于正在构建的应用程序类型。请记住，[`Session`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")它只是对象的工作空间，是特定数据库连接的本地工作空间 - 如果您将应用程序线程视为晚宴[`Session`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session") 上的访客，则是客人的盘子，它所拥有的对象是食物（和数据库......厨房？）！有关此主题的更多信息，请参阅[何时构建会话，何时提交会话以及何时关闭会话？](http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#session-faq-whentocreate)。

这个定制[`Session`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")类将创建[`Session`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")绑定到我们数据库的新对象。调用时也可以定义其他事务特征[`sessionmaker`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.sessionmaker "sqlalchemy.orm.session.sessionmaker"); 这些将在后面的章节中描述。然后，只要您需要与数据库进行对话，就可以实例化[`Session`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> session = Session()</pre>

以上[`Session`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")内容与我们的SQLite相关联[`Engine`](http://docs.sqlalchemy.org/en/latest/core/connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")，但尚未打开任何连接。当它第一次使用时，它从由[`Engine`](http://docs.sqlalchemy.org/en/latest/core/connections.html#sqlalchemy.engine.Engine "sqlalchemy.engine.Engine")它维护的连接池中检索连接 ，并保持它，直到我们提交所有更改和/或关闭会话对象。

## 添加和更新对象[](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#adding-and-updating-objects "永久链接到这个标题")

为了坚持我们的`User`目标，我们[`add()`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session.add "sqlalchemy.orm.session.Session.add")对我们[`Session`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
>>> session.add(ed_user)</pre>

此时，我们说该实例正在**等待** ; 尚未发布任何SQL，并且该对象尚未由数据库中的行表示。该 [`Session`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")会发出SQL坚持，只要需要，使用被称为一个过程**冲洗**。如果我们查询数据库，则首先刷新所有待处理信息，然后立即发出查询。`Ed Jones``Ed Jones`

例如，下面我们创建一个[`Query`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")加载实例的新对象`User`。我们“过滤” `name`属性 `ed`，并表示我们只想要完整行列表中的第一个结果。`User`返回一个实例，它等同于我们添加的实例：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> our_user = session.query(User).filter_by(name='ed').first() 
>>> our_user
<User(name='ed', fullname='Ed Jones', password='edspassword')></pre>

实际上，[`Session`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")已经确定返回的行与在其内部对象映射中已经表示的行**相同**，因此我们实际上得到了与我们刚刚添加的实例相同的实例：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> ed_user is our_user
True</pre>

这里工作的ORM概念称为[身份映射，](http://docs.sqlalchemy.org/en/latest/glossary.html#term-identity-map) 并确保在一个特定行上的所有操作都在 [`Session`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")同一组数据上运行。一旦具有特定主键的对象存在于其中 [`Session`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")，则所有SQL查询 [`Session`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")将始终返回该特定主键的相同Python对象; 如果尝试在会话中放置具有相同主键的第二个已经持久化的对象，它也会引发错误。

我们可以`User`一次添加更多对象 [`add_all()`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session.add_all "sqlalchemy.orm.session.Session.add_all")：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> session.add_all([
...     User(name='wendy', fullname='Wendy Williams', password='foobar'),
...     User(name='mary', fullname='Mary Contrary', password='xxg527'),
...     User(name='fred', fullname='Fred Flinstone', password='blah')])</pre>

此外，我们已经确定Ed的密码不太安全，所以我们改变它：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> ed_user.password = 'f8s7ccs'</pre>

该[`Session`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")被关注。例如，它知道已被修改：`Ed Jones`

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> session.dirty
IdentitySet([<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>])</pre>

并且有三个新`User`对象待定：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> session.new  
IdentitySet([<User(name='wendy', fullname='Wendy Williams', password='foobar')>,
<User(name='mary', fullname='Mary Contrary', password='xxg527')>,
<User(name='fred', fullname='Fred Flinstone', password='blah')>])</pre>

我们告诉我们[`Session`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")，我们想要对数据库发出所有剩余的更改并提交事务，该事务一直在进行中。我们通过这样做[`commit()`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")。在 [`Session`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")发出`UPDATE`关于“ED”的密码更改，以及声明`INSERT`三个新语句`User`我们添加的对象：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> session.commit()
</pre>

[`commit()`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")刷新对数据库的剩余更改，并提交事务。会话引用的连接资源现在返回到连接池。此会话的后续操作将在**新**事务中进行，该事务将在首次需要时再次重新获取连接资源。

如果我们看看之前的Ed `id`属性`None`，它现在有一个值：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> ed_user.id 
1</pre>

在[`Session`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")数据库中插入新行后，所有新生成的标识符和数据库生成的默认值都可以立即在实例上使用，也可以通过首次访问加载来实现。在这种情况下，整个行在访问时被重新加载，因为在我们发布之后开始了新的事务[`commit()`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session.commit "sqlalchemy.orm.session.Session.commit")。默认情况下，SQLAlchemy会在第一次在新事务中访问时刷新先前事务中的数据，以便最新状态可用。重新加载的级别是可配置的，如[使用会话中所述](http://docs.sqlalchemy.org/en/latest/orm/session.html)。

会话对象状态

当我们的`User`对象从外部移动[`Session`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")到[`Session`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")没有主键的内部，实际被插入时，它在四个可用的“对象状态”中的三个之间移动 - **瞬态**，**待定**和**持久**。了解这些状态及其含义总是一个好主意 - 请务必阅读[Quickie Intro to Object States](http://docs.sqlalchemy.org/en/latest/orm/session_state_management.html#session-object-states)以获得快速概述。

## 回滚[](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#rolling-back "永久链接到这个标题")

由于[`Session`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")交易中的工作，我们也可以回滚所做的更改。让我们做两个我们将要改变的变化; `ed_user`的用户名设置为`Edwardo`：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> ed_user.name = 'Edwardo'</pre>

我们将添加另一个错误的用户，`fake_user`：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> fake_user = User(name='fakeuser', fullname='Invalid', password='12345')
>>> session.add(fake_user)</pre>

查询会话，我们可以看到它们被刷新到当前事务中：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all()
[<User(name='Edwardo', fullname='Ed Jones', password='f8s7ccs')>, <User(name='fakeuser', fullname='Invalid', password='12345')>]</pre>

回滚过去，我们可以看到这个`ed_user`名字又回来了`ed`，并且 `fake_user`已经被踢出了会议：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> session.rollback()

[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> ed_user.name
u'ed'
>>> fake_user in session
False</pre>

发出SELECT说明了对数据库所做的更改：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> session.query(User).filter(User.name.in_(['ed', 'fakeuser'])).all()
[<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>]</pre>

## 查询[](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#querying "永久链接到这个标题")

甲[`Query`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象使用所创建的 [`query()`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session.query "sqlalchemy.orm.session.Session.query")上方法 [`Session`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")。此函数采用可变数量的参数，可以是类和类检测描述符的任意组合。下面，我们指出 [`Query`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")哪个加载`User`实例。在迭代上下文中计算时，将`User`返回存在的对象列表：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> for instance in session.query(User).order_by(User.id):
...     print(instance.name, instance.fullname)
ed Ed Jones
wendy Wendy Williams
mary Mary Contrary
fred Fred Flinstone</pre>

该[`Query`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")还接受ORM，仪表描述作为参数。每当多个类实体或基于列的实体表示为函数的参数时 [`query()`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session.query "sqlalchemy.orm.session.Session.query")，返回结果表示为元组：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> for name, fullname in session.query(User.name, User.fullname):
...     print(name, fullname)
ed Ed Jones
wendy Wendy Williams
mary Mary Contrary
fred Fred Flinstone</pre>

返回的元组[`Query`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")被*命名为* 元组，由[`KeyedTuple`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.util.KeyedTuple "sqlalchemy.util.KeyedTuple")类提供，并且可以像普通的Python对象一样对待。名称与属性的属性名称以及类的类名称相同：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> for row in session.query(User, User.name).all():
...    print(row.User, row.name)
<User(name='ed', fullname='Ed Jones', password='f8s7ccs')> ed
<User(name='wendy', fullname='Wendy Williams', password='foobar')> wendy
<User(name='mary', fullname='Mary Contrary', password='xxg527')> mary
<User(name='fred', fullname='Fred Flinstone', password='blah')> fred</pre>

您可以使用[`label()`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.label "sqlalchemy.sql.expression.ColumnElement.label")构造控制单个列表达式的名称，该 构造可从任何[`ColumnElement`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement "sqlalchemy.sql.expression.ColumnElement")派生对象获得，以及映射到其中的任何类属性（例如`User.name`）：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> for row in session.query(User.name.label('name_label')).all():
...    print(row.name_label)
ed
wendy
mary
fred</pre>

给予完整实体的名称，例如`User`，假设调用中存在多个实体[`query()`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session.query "sqlalchemy.orm.session.Session.query")，可以使用[`aliased()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased")以下方法控制 ：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> from sqlalchemy.orm import aliased
>>> user_alias = aliased(User, name='user_alias')

[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> for row in session.query(user_alias, user_alias.name).all():
...    print(row.user_alias)
<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>
<User(name='wendy', fullname='Wendy Williams', password='foobar')>
<User(name='mary', fullname='Mary Contrary', password='xxg527')>
<User(name='fred', fullname='Fred Flinstone', password='blah')></pre>

基本操作[`Query`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")包括发出LIMIT和OFFSET，最方便的是使用Python数组切片，通常与ORDER BY结合使用：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> for u in session.query(User).order_by(User.id)[1:3]:
...    print(u)
<User(name='wendy', fullname='Wendy Williams', password='foobar')>
<User(name='mary', fullname='Mary Contrary', password='xxg527')></pre>

和过滤结果，使用 [`filter_by()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.filter_by "sqlalchemy.orm.query.Query.filter_by")，使用关键字参数完成：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> for name, in session.query(User.name).\
...             filter_by(fullname='Ed Jones'):
...    print(name)
ed</pre>

...或者[`filter()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.filter "sqlalchemy.orm.query.Query.filter")，它使用更灵活的SQL表达式语言结构。这些允许您使用常规Python运算符和映射类的类级属性：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> for name, in session.query(User.name).\
...             filter(User.fullname=='Ed Jones'):
...    print(name)
ed</pre>

该[`Query`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")对象是完全**生成的**，这意味着大多数方法调用返回一个新[`Query`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query") 对象，可以在其上添加进一步的标准。例如，要查询名为“ed”且名称为“Ed Jones”的用户，可以调用 [`filter()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.filter "sqlalchemy.orm.query.Query.filter")两次，使用`AND`以下命令连接条件 ：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> for user in session.query(User).\
...          filter(User.name=='ed').\
...          filter(User.fullname=='Ed Jones'):
...    print(user)
<User(name='ed', fullname='Ed Jones', password='f8s7ccs')></pre>

### 通用过滤器运算符[](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#common-filter-operators "永久链接到这个标题")

以下是一些最常用的运算符的概述 [`filter()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.filter "sqlalchemy.orm.query.Query.filter")：

*   [`equals`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__eq__ "sqlalchemy.sql.operators.ColumnOperators .__ eq__")：

    <pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">query.filter(User.name == 'ed')</pre>

*   [`not equals`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__ne__ "sqlalchemy.sql.operators.ColumnOperators .__ ne__")：

    <pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">query.filter(User.name != 'ed')</pre>

*   [`LIKE`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")：

    <pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">query.filter(User.name.like('%ed%'))</pre>

> 注意
> 
> [`ColumnOperators.like()`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like "sqlalchemy.sql.operators.ColumnOperators.like")呈现LIKE运算符，对某些后端不区分大小写，对其他后端区分大小写。对于保证不区分大小写的比较，请使用[`ColumnOperators.ilike()`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")。

*   [`ILIKE`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike") （不区分大小写的LIKE）：

    <pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">query.filter(User.name.ilike('%ed%'))</pre>

> 注意
> 
> 大多数后端不直接支持ILIKE。对于那些，[`ColumnOperators.ilike()`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.ilike "sqlalchemy.sql.operators.ColumnOperators.ilike")运算符呈现一个表达式，将LIKE与应用于每个操作数的LOWER SQL函数相结合。

*   [`IN`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.in_ "sqlalchemy.sql.operators.ColumnOperators.in_")：

    <pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">query.filter(User.name.in_(['ed', 'wendy', 'jack']))

    # works with query objects too:
    query.filter(User.name.in_(
        session.query(User.name).filter(User.name.like('%ed%'))
    ))</pre>

*   [`NOT IN`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.notin_ "sqlalchemy.sql.operators.ColumnOperators.notin_")：

    <pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">query.filter(~User.name.in_(['ed', 'wendy', 'jack']))</pre>

*   [`IS NULL`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.is_ "sqlalchemy.sql.operators.ColumnOperators.is_")：

    <pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">query.filter(User.name == None)

    # alternatively, if pep8/linters are a concern
    query.filter(User.name.is_(None))</pre>

*   [`IS NOT NULL`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.isnot "sqlalchemy.sql.operators.ColumnOperators.isnot")：

    <pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">query.filter(User.name != None)

    # alternatively, if pep8/linters are a concern
    query.filter(User.name.isnot(None))</pre>

*   [`AND`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.expression.and_ "sqlalchemy.sql.expression.and_")：

    <pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;"># use and_()
    from sqlalchemy import and_
    query.filter(and_(User.name == 'ed', User.fullname == 'Ed Jones'))

    # or send multiple expressions to .filter()
    query.filter(User.name == 'ed', User.fullname == 'Ed Jones')

    # or chain multiple filter()/filter_by() calls
    query.filter(User.name == 'ed').filter(User.fullname == 'Ed Jones')</pre>

> 注意
> 
> 确保使用[`and_()`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.expression.and_ "sqlalchemy.sql.expression.and_")而**不是** Python `and`运算符！

*   [`OR`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.expression.or_ "sqlalchemy.sql.expression.or_")：

    <pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">from sqlalchemy import or_
    query.filter(or_(User.name == 'ed', User.name == 'wendy'))</pre>

> 注意
> 
> 确保使用[`or_()`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.expression.or_ "sqlalchemy.sql.expression.or_")而**不是** Python `or`运算符！

*   [`MATCH`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.match "sqlalchemy.sql.operators.ColumnOperators.match")：

    <pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">query.filter(User.name.match('wendy'))</pre>

> 注意
> 
> [`match()`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.match "sqlalchemy.sql.operators.ColumnOperators.match")使用特定于数据库`MATCH` 或`CONTAINS`函数; 它的行为会因后端而异，并且在某些后端（例如SQLite）上不可用。

### 返回列表和标量[](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#returning-lists-and-scalars "永久链接到这个标题")

有许多方法可以[`Query`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query") 立即发出SQL并返回包含已加载数据库结果的值。这是一个简短的旅游：

*   [`all()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.all "sqlalchemy.orm.query.Query.all") 返回一个列表：

    <pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> query = session.query(User).filter(User.name.like('%ed')).order_by(User.id)
    [SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> query.all()
    [<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>,
          <User(name='fred', fullname='Fred Flinstone', password='blah')>]</pre>

*   [`first()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.first "sqlalchemy.orm.query.Query.first") 应用限制为1并将第一个结果作为标量返回：

    <pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> query.first()
    <User(name='ed', fullname='Ed Jones', password='f8s7ccs')></pre>

*   [`one()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.one "sqlalchemy.orm.query.Query.one")完全提取所有行，如果结果中不存在一个对象标识或复合行，则会引发错误。找到多行：

    <pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> user = query.one()
    Traceback (most recent call last):
    ...
    MultipleResultsFound: Multiple rows were found for one()</pre>

    没有找到行：

    <pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> user = query.filter(User.id == 99).one()
    Traceback (most recent call last):
    ...
    NoResultFound: No row was found for one()</pre>

    该[`one()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.one "sqlalchemy.orm.query.Query.one")方法非常适用于希望处理“找不到物品”而不是“找到多件物品”的系统; 例如RESTful Web服务，可能希望在找不到结果时引发“未找到404”，但在找到多个结果时引发应用程序错误。

*   [`one_or_none()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.one_or_none "sqlalchemy.orm.query.Query.one_or_none")就像[`one()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.one "sqlalchemy.orm.query.Query.one")，除非没有找到结果，它不会引起错误; 它只是回来了`None`。像 [`one()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.one "sqlalchemy.orm.query.Query.one")，但是，它如果有多个结果发现引发错误。

*   [`scalar()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.scalar "sqlalchemy.orm.query.Query.scalar")调用该[`one()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.one "sqlalchemy.orm.query.Query.one")方法，并在成功时返回该行的第一列：

    <pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> query = session.query(User.id).filter(User.name == 'ed').\
    ...    order_by(User.id)
    [SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> query.scalar()
    1</pre>

### 使用文本[](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#using-textual-sql "永久链接到这个标题")

[`Query`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")通过指定它们对[`text()`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")构造的使用，可以灵活地使用文字字符串 ，这是大多数适用方法所接受的。例如， [`filter()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.filter "sqlalchemy.orm.query.Query.filter")和 [`order_by()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.order_by "sqlalchemy.orm.query.Query.order_by")：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> from sqlalchemy import text
[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> for user in session.query(User).\
...             filter(text("id<224")).\
...             order_by(text("id")).all():
...     print(user.name)
ed
wendy
mary
fred</pre>

可以使用冒号使用基于字符串的SQL指定绑定参数。要指定值，请使用以下[`params()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.params "sqlalchemy.orm.query.Query.params") 方法：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> session.query(User).filter(text("id<:value and name=:name")).\
...     params(value=224, name='fred').order_by(User.id).one()
<User(name='fred', fullname='Fred Flinstone', password='blah')></pre>

要使用完全基于字符串的语句，[`text()`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")可以将表示完整语句的构造传递给 [`from_statement()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.from_statement "sqlalchemy.orm.query.Query.from_statement")。如果没有其他说明符，字符串SQL中的列将根据名称与模型列匹配，例如下面我们只使用星号表示加载所有列：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> session.query(User).from_statement(
...                     text("SELECT * FROM users where name=:name")).\
...                     params(name='ed').all()
[<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>]</pre>

匹配名称上的列适用于简单的情况，但在处理包含重复列名的复杂语句或使用不易与特定名称匹配的匿名ORM构造时可能会变得难以处理。此外，在处理结果行时，我们可能会发现在映射列中存在键入行为。对于这些情况，[`text()`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")构造允许我们在位置上将其文本SQL链接到Core或ORM映射的列表达式; 我们可以通过将列表达式作为位置参数传递给[`TextClause.columns()`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")方法来实现这一点 ：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> stmt = text("SELECT name, id, fullname, password "
...             "FROM users where name=:name")
>>> stmt = stmt.columns(User.name, User.id, User.fullname, User.password)
[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> session.query(User).from_statement(stmt).params(name='ed').all()
[<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>]</pre>

版本1.1中的新增功能：该[`TextClause.columns()`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.expression.TextClause.columns "sqlalchemy.sql.expression.TextClause.columns")方法现在接受列表达式，这些列表达式将与纯文本SQL结果集进行位置匹配，从而无需在SQL语句中匹配甚至是唯一的列名。

从[`text()`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")构造中进行选择时，[`Query`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query") 仍然可以指定要返回的列和实体; 而不是 `query(User)`我们也可以单独要求列，如在任何其他情况下：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> stmt = text("SELECT name, id FROM users where name=:name")
>>> stmt = stmt.columns(User.name, User.id)
[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> session.query(User.id, User.name).\
...          from_statement(stmt).params(name='ed').all()
[(1, u'ed')]</pre>

也可以看看

[使用Textual SQL](http://docs.sqlalchemy.org/en/latest/core/tutorial.html#sqlexpression-text) -[`text()`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.expression.text "sqlalchemy.sql.expression.text")从仅核心查询的角度解释构造。

### 计数[](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#counting "永久链接到这个标题")

[`Query`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")包括一种方便的计数方法[`count()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.count "sqlalchemy.orm.query.Query.count")：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> session.query(User).filter(User.name.like('%ed')).count()
2</pre>

指望 `count()`

[`Query.count()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.count "sqlalchemy.orm.query.Query.count")曾经是一个非常复杂的方法，当它试图猜测现有查询周围是否需要子查询时，在某些奇特的情况下它不会做正确的事情。现在它每次都使用一个简单的子查询，它只有两行长并且总是返回正确的答案。使用`func.count()`如果一个特定的语句绝对不能容忍的子查询存在。

该[`count()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.count "sqlalchemy.orm.query.Query.count")方法用于确定SQL语句将返回多少行。查看上面生成的SQL，SQLAlchemy总是将我们查询的任何内容放入子查询中，然后从中计算行数。在某些情况下，这可以简化为更简单，但SQLAlchemy的现代版本不会尝试猜测何时合适，因为可以使用更明确的方法发出确切的SQL。`SELECT count(*) FROM table`

对于需要具体指出“要计数的东西”的情况，我们可以直接使用构造中`func.count()`可用 的表达式指定“计数”函数[`func`](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.expression.func "sqlalchemy.sql.expression.func")。下面我们用它来返回每个不同用户名的计数：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> from sqlalchemy import func
[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> session.query(func.count(User.name), User.name).group_by(User.name).all()
[(1, u'ed'), (1, u'fred'), (1, u'mary'), (1, u'wendy')]</pre>

为了实现我们的简单，我们可以将其应用为：`SELECT count(*) FROM table`

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> session.query(func.count('*')).select_from(User).scalar()
4</pre>

[`select_from()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.select_from "sqlalchemy.orm.query.Query.select_from")如果我们`User`直接用主键表示计数，则可以删除用法：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> session.query(func.count(User.id)).scalar()
4</pre>

## 建立关系[](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#building-a-relationship "永久链接到这个标题")

让我们考虑如何`User`映射和查询与之相关的第二个表。我们系统中的用户可以存储与其用户名关联的任意数量的电子邮件地址。这意味着从`users`存储电子邮件地址的新表到基本的一对多关联，我们将调用它`addresses`。使用声明，我们将此表及其映射类定义为`Address`：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> from sqlalchemy import ForeignKey
>>> from sqlalchemy.orm import relationship

>>> class Address(Base):
...     __tablename__ = 'addresses'
...     id = Column(Integer, primary_key=True)
...     email_address = Column(String, nullable=False)
...     user_id = Column(Integer, ForeignKey('users.id'))
...
...     user = relationship("User", back_populates="addresses")
...
...     def __repr__(self):
...         return "<Address(email_address='%s')>" % self.email_address

>>> User.addresses = relationship(
...     "Address", order_by=Address.id, back_populates="user")</pre>

上面的类介绍了[`ForeignKey`](http://docs.sqlalchemy.org/en/latest/core/constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")构造，它是一个应用于的指令，[`Column`](http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")它指示此列中的值应该被[约束](http://docs.sqlalchemy.org/en/latest/glossary.html#term-constrained)为指定的远程列中存在的值。这是关系数据库的核心功能，并且是“粘合剂”，它将未连接的表集合转换为具有丰富的重叠关系。的[`ForeignKey`](http://docs.sqlalchemy.org/en/latest/core/constraints.html#sqlalchemy.schema.ForeignKey "sqlalchemy.schema.ForeignKey")是，在以上的值表示`addresses.user_id`列应被约束在这些值`users.id`列中，即它的主键。

第二个指令，称为[`relationship()`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")ORM ，使用该属性告诉ORM `Address`类本身应该链接到`User`类`Address.user`。 [`relationship()`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")使用两个表之间的外键关系来确定此链接的性质，确定`Address.user`将是[多对一](http://docs.sqlalchemy.org/en/latest/glossary.html#term-many-to-one)。另一个[`relationship()`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")指令放在 `User`属性下的映射类中`User.addresses`。在两个 [`relationship()`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")指令中，[`relationship.back_populates`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates "sqlalchemy.orm.relationship")分配参数 以引用补充属性名称; 通过这样做，每个人都[`relationship()`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship") 可以做出与反向表达的相同关系的智能决策; 一方面，`Address.user`指的是一个`User`实例，另一方面`User.addresses`指的是一个列表 `Address` 实例。

注意

该[`relationship.back_populates`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates "sqlalchemy.orm.relationship")参数是一个非常常见的SQLAlchemy功能的较新版本 [`relationship.backref`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship.params.backref "sqlalchemy.orm.relationship")。该[`relationship.backref`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship.params.backref "sqlalchemy.orm.relationship") 参数还没有到哪里去了，永远保持可用！这[`relationship.back_populates`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates "sqlalchemy.orm.relationship")是一回事，除了更冗长，更容易操纵。有关整个主题的概述，请参阅[使用Backref链接关系](http://docs.sqlalchemy.org/en/latest/orm/backref.html#relationships-backref)部分。

多对一关系的反面总是[一对多](http://docs.sqlalchemy.org/en/latest/glossary.html#term-one-to-many)。[基本关系模式的](http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#relationship-patterns)完整可用[`relationship()`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")配置目录。[](http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#relationship-patterns)

两个互补关系`Address.user`并且`User.addresses` 被称为一个[双向关系](http://docs.sqlalchemy.org/en/latest/glossary.html#term-bidirectional-relationship)，并且是SQLAlchemy的ORM的一个关键特征。[Linking Relationships with Backref](http://docs.sqlalchemy.org/en/latest/orm/backref.html#relationships-backref)部分[详细](http://docs.sqlalchemy.org/en/latest/orm/backref.html#relationships-backref) 讨论了“backref”功能。

[`relationship()`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")假设声明系统正在使用中，可以使用字符串指定远程类所关注的参数。一旦所有映射完成，这些字符串将被计算为Python表达式，以便生成实际参数，在上面的例子中是`User`类。在此评估期间允许使用的名称包括根据声明的基础创建的所有类的名称。

有关[`relationship()`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")参数样式的更多详细信息，请参阅docstring 。

你知道吗 ？

*   大多数（尽管不是全部）关系数据库中的FOREIGN KEY约束只能链接到主键列或具有UNIQUE约束的列。
*   引用多列主键的FOREIGN KEY约束，本身有多列，称为“复合外键”。它还可以引用这些列的子集。
*   FOREIGN KEY列可以自动更新，以响应引用的列或行的更改。这称为CASCADE *引用操作*，是关系数据库的内置函数。
*   FOREIGN KEY可以参考自己的表。这被称为“自引用”外键。
*   在外键[- 维基百科上](http://en.wikipedia.org/wiki/Foreign_key)阅读更多关于外键的信息。

我们需要`addresses`在数据库中创建表，因此我们将从元数据中发出另一个CREATE，它将跳过已经创建的表：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> Base.metadata.create_all(engine)
</pre>

## 使用相关对象[](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#working-with-related-objects "永久链接到这个标题")

现在，当我们创建一个`User`空白`addresses`集合时，将会出现。此处可以使用各种集合类型（例如集和字典）（有关详细信息，请参阅[自定义集合访问](http://docs.sqlalchemy.org/en/latest/orm/collections.html#custom-collections)），但默认情况下，集合是Python列表。

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> jack = User(name='jack', fullname='Jack Bean', password='gjffdd')
>>> jack.addresses
[]</pre>

我们可以自由地在`Address`对象上添加`User`对象。在这种情况下，我们只是直接指定一个完整列表：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> jack.addresses = [
...                 Address(email_address='jack@google.com'),
...                 Address(email_address='j25@yahoo.com')]</pre>

使用双向关系时，在一个方向上添加的元素会自动在另一个方向上可见。此行为基于属性on-change事件发生，并在Python中进行评估，而不使用任何SQL：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> jack.addresses[1]
<Address(email_address='j25@yahoo.com')>

>>> jack.addresses[1].user
<User(name='jack', fullname='Jack Bean', password='gjffdd')></pre>

让我们添加并提交到数据库。以及相应 集合中的两个成员都使用称为**级联**的过程一次添加到会话中：`Jack Bean``jack``Address``addresses`

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> session.add(jack)
[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> session.commit()
</pre>

查询杰克，我们得到杰克回来。尚未为Jack的地址发布SQL：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> jack = session.query(User).\
... filter_by(name='jack').one()
>>> jack
<User(name='jack', fullname='Jack Bean', password='gjffdd')></pre>

我们来看看这个`addresses`系列吧。观看SQL：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> jack.addresses
[<Address(email_address='jack@google.com')>, <Address(email_address='j25@yahoo.com')>]</pre>

当我们访问`addresses`集合时，突然发出了SQL。这是[延迟加载](http://docs.sqlalchemy.org/en/latest/glossary.html#term-lazy-loading)关系的一个例子。该`addresses`集合现在已加载，其行为就像普通列表一样。我们将介绍一些优化加载这个集合的方法。

## 用连接查询[](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#querying-with-joins "永久链接到这个标题")

现在我们有两个表，我们可以显示更多的功能[`Query`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")，特别是如何创建同时处理这两个表的查询。[SQL JOIN上](http://en.wikipedia.org/wiki/Join_%28SQL%29)的[Wikipedia页面](http://en.wikipedia.org/wiki/Join_%28SQL%29)提供了对连接技术的一个很好的介绍，其中几个我们将在这里说明。

要在`User`和之间构造一个简单的隐式连接`Address`，我们可以使用[`Query.filter()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.filter "sqlalchemy.orm.query.Query.filter")它们将它们的相关列等同起来。下面我们使用这个方法一次加载`User`和`Address`实体：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> for u, a in session.query(User, Address).\
...                     filter(User.id==Address.user_id).\
...                     filter(Address.email_address=='jack@google.com').\
...                     all():
...     print(u)
...     print(a)
<User(name='jack', fullname='Jack Bean', password='gjffdd')>
<Address(email_address='jack@google.com')></pre>

另一方面，实际的SQL JOIN语法最容易使用以下[`Query.join()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")方法实现：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> session.query(User).join(Address).\
...         filter(Address.email_address=='jack@google.com').\
...         all()
[<User(name='jack', fullname='Jack Bean', password='gjffdd')>]</pre>

[`Query.join()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")知道如何加入`User` ，`Address`因为它们之间只有一个外键。如果没有外键或多个外键，[`Query.join()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join") 则在使用以下表单之一时效果更好：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">query.join(Address, User.id==Address.user_id)    # explicit condition
query.join(User.addresses)                       # specify relationship from left to right
query.join(Address, User.addresses)              # same, with explicit target
query.join('addresses')                          # same, using a string</pre>

正如您所期望的那样，使用以下[`outerjoin()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.outerjoin "sqlalchemy.orm.query.Query.outerjoin")函数将相同的想法用于“外部”连接 ：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">query.outerjoin(User.addresses)   # LEFT OUTER JOIN</pre>

参考文档[`join()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")包含此方法接受的调用样式的详细信息和示例; [`join()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join") 对于任何SQL-fluent应用程序而言，它是使用中心的重要方法。

[`Query`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")如果有多个实体，可以选择什么？

当省略ON子句或ON子句是纯SQL表达式时，该[`Query.join()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")方法**通常从**实体列表中**最左边的项加入**。要控制JOIN列表中的第一个实体，请使用以下[`Query.select_from()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.select_from "sqlalchemy.orm.query.Query.select_from")方法：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">query = session.query(User, Address).select_from(Address).join(User)</pre>

### 使用别名[](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#using-aliases "永久链接到这个标题")

在跨多个表进行查询时，如果需要多次引用同一个表，则SQL通常要求使用其他名称对该表进行*别名*，以便可以将该表与该表的其他实例区分开来。[`Query`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")最明确使用[`aliased`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.aliased "sqlalchemy.orm.aliased")构造的支持。下面我们`Address` 两次加入实体，找到同时拥有两个不同电子邮件地址的用户：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> from sqlalchemy.orm import aliased
>>> adalias1 = aliased(Address)
>>> adalias2 = aliased(Address)
[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> for username, email1, email2 in \
...     session.query(User.name, adalias1.email_address, adalias2.email_address).\
...     join(adalias1, User.addresses).\
...     join(adalias2, User.addresses).\
...     filter(adalias1.email_address=='jack@google.com').\
...     filter(adalias2.email_address=='j25@yahoo.com'):
...     print(username, email1, email2)
jack jack@google.com j25@yahoo.com</pre>

### 使用子查询[](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#using-subqueries "永久链接到这个标题")

的[`Query`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")是适合于产生其可以被用作子查询语句。假设我们想要加载`User`对象以及`Address`每个用户拥有多少条记录的计数。生成这样的SQL的最佳方法是获取按用户ID分组的地址计数，并将JOIN连接到父级。在这种情况下，我们使用LEFT OUTER JOIN，以便为没有任何地址的用户返回行，例如：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">SELECT users.*, adr_count.address_count FROM users LEFT OUTER JOIN
    (SELECT user_id, count(*) AS address_count
        FROM addresses GROUP BY user_id) AS adr_count
    ON users.id=adr_count.user_id</pre>

使用[`Query`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")，我们从内到外构建一个这样的语句。的`statement`存取器返回一个表示由特定生成的声明SQL表达式 [`Query`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")-这是一个实例[`select()`](http://docs.sqlalchemy.org/en/latest/core/selectable.html#sqlalchemy.sql.expression.select "sqlalchemy.sql.expression.select") 构建体，其中描述了[SQL表达式语言教程](http://docs.sqlalchemy.org/en/latest/core/tutorial.html)：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> from sqlalchemy.sql import func
>>> stmt = session.query(Address.user_id, func.count('*').\
...         label('address_count')).\
...         group_by(Address.user_id).subquery()</pre>

所述`func`关键字生成SQL函数，以及`subquery()`关于方法 [`Query`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")产生表示嵌入的别名内SELECT语句中的SQL表达构建体（它实际上是简写`query.statement.alias()`）。

一旦我们得到了语句，它就像一个[`Table`](http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")构造，比如我们在`users`本教程开始时创建的 构造 。语句中的列可通过以下属性访问`c`：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> for u, count in session.query(User, stmt.c.address_count).\
...     outerjoin(stmt, User.id==stmt.c.user_id).order_by(User.id):
...     print(u, count)
<User(name='ed', fullname='Ed Jones', password='f8s7ccs')> None
<User(name='wendy', fullname='Wendy Williams', password='foobar')> None
<User(name='mary', fullname='Mary Contrary', password='xxg527')> None
<User(name='fred', fullname='Fred Flinstone', password='blah')> None
<User(name='jack', fullname='Jack Bean', password='gjffdd')> 2</pre>

### 从子查询中选择实体[](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#selecting-entities-from-subqueries "永久链接到这个标题")

上面，我们刚刚选择了一个包含子查询列的结果。如果我们希望子查询映射到实体怎么办？为此，我们使用`aliased()` 将映射类的“别名”与子查询相关联：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> stmt = session.query(Address).\
...                 filter(Address.email_address != 'j25@yahoo.com').\
...                 subquery()
>>> adalias = aliased(Address, stmt)
>>> for user, address in session.query(User, adalias).\
...         join(adalias, User.addresses):
...     print(user)
...     print(address)
<User(name='jack', fullname='Jack Bean', password='gjffdd')>
<Address(email_address='jack@google.com')></pre>

### 使用[](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#using-exists "永久链接到这个标题")

SQL中的EXISTS关键字是一个布尔运算符，如果给定的表达式包含任何行，则返回True。它可以在许多场景中用于代替连接，也可用于定位在相关表中没有相应行的行。

有一个显式的EXISTS结构，如下所示：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> from sqlalchemy.sql import exists
>>> stmt = exists().where(Address.user_id==User.id)
[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> for name, in session.query(User.name).filter(stmt):
...     print(name)
jack</pre>

该[`Query`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")功能几家运营商，这使得使用情况自动存在。上面，声明可以`User.addresses`使用[`any()`](http://docs.sqlalchemy.org/en/latest/orm/internals.html#sqlalchemy.orm.properties.RelationshipProperty.Comparator.any "sqlalchemy.orm.properties.RelationshipProperty.Comparator.any")以下关系表达 ：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> for name, in session.query(User.name).\
...         filter(User.addresses.any()):
...     print(name)
jack</pre>

[`any()`](http://docs.sqlalchemy.org/en/latest/orm/internals.html#sqlalchemy.orm.properties.RelationshipProperty.Comparator.any "sqlalchemy.orm.properties.RelationshipProperty.Comparator.any") 采用标准，限制匹配的行：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> for name, in session.query(User.name).\
...     filter(User.addresses.any(Address.email_address.like('%google%'))):
...     print(name)
jack</pre>

[`has()`](http://docs.sqlalchemy.org/en/latest/orm/internals.html#sqlalchemy.orm.properties.RelationshipProperty.Comparator.has "sqlalchemy.orm.properties.RelationshipProperty.Comparator.has")与[`any()`](http://docs.sqlalchemy.org/en/latest/orm/internals.html#sqlalchemy.orm.properties.RelationshipProperty.Comparator.any "sqlalchemy.orm.properties.RelationshipProperty.Comparator.any")多对一关系是同一个运算符 （请注意`~`这里的运算符，这意味着“NOT”）：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> session.query(Address).\
...         filter(~Address.user.has(User.name=='jack')).all()
[]</pre>

### 公共关系运算符[](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#common-relationship-operators "永久链接到这个标题")

以下是构建关系的所有运算符 - 每个运算符都链接到其API文档，其中包含有关使用和行为的完整详细信息：

*   [`__eq__()`](http://docs.sqlalchemy.org/en/latest/orm/internals.html#sqlalchemy.orm.properties.RelationshipProperty.Comparator.__eq__ "sqlalchemy.orm.properties.RelationshipProperty.Comparator .__ eq__") （多对一“等于”比较）：

    <pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">query.filter(Address.user == someuser)</pre>

*   [`__ne__()`](http://docs.sqlalchemy.org/en/latest/orm/internals.html#sqlalchemy.orm.properties.RelationshipProperty.Comparator.__ne__ "sqlalchemy.orm.properties.RelationshipProperty.Comparator .__ ne__") （多对一“不等于”比较）：

    <pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">query.filter(Address.user != someuser)</pre>

*   IS NULL（多对一比较，也使用[`__eq__()`](http://docs.sqlalchemy.org/en/latest/orm/internals.html#sqlalchemy.orm.properties.RelationshipProperty.Comparator.__eq__ "sqlalchemy.orm.properties.RelationshipProperty.Comparator .__ eq__")）：

    <pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">query.filter(Address.user == None)</pre>

*   [`contains()`](http://docs.sqlalchemy.org/en/latest/orm/internals.html#sqlalchemy.orm.properties.RelationshipProperty.Comparator.contains "sqlalchemy.orm.properties.RelationshipProperty.Comparator.contains") （用于一对多收藏）：

    <pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">query.filter(User.addresses.contains(someaddress))</pre>

*   [`any()`](http://docs.sqlalchemy.org/en/latest/orm/internals.html#sqlalchemy.orm.properties.RelationshipProperty.Comparator.any "sqlalchemy.orm.properties.RelationshipProperty.Comparator.any") （用于收藏）：

    <pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">query.filter(User.addresses.any(Address.email_address == 'bar'))

    # also takes keyword arguments:
    query.filter(User.addresses.any(email_address='bar'))</pre>

*   [`has()`](http://docs.sqlalchemy.org/en/latest/orm/internals.html#sqlalchemy.orm.properties.RelationshipProperty.Comparator.has "sqlalchemy.orm.properties.RelationshipProperty.Comparator.has") （用于标量引用）：

    <pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">query.filter(Address.user.has(name='ed'))</pre>

*   [`Query.with_parent()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.with_parent "sqlalchemy.orm.query.Query.with_parent") （用于任何关系）：

    <pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">session.query(Address).with_parent(someuser, 'addresses')</pre>

## 渴望加载[](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#eager-loading "永久链接到这个标题")

回想一下，当我们访问a的集合并发出SQL 时，我们说明了一个[延迟加载](http://docs.sqlalchemy.org/en/latest/glossary.html#term-lazy-loading)操作。如果您想减少查询数量（在很多情况下显着），我们可以对查询操作应用急切加载。SQLAlchemy提供三种类型的预先加载，其中两种是自动加载，第三种涉及自定义标准。所有这三个通常都是通过称为查询选项的函数调用的，这些函数通过该方法为我们希望如何加载各种属性提供了额外的指令。`User.addresses``User`[`Query`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")[`Query.options()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.options "sqlalchemy.orm.query.Query.options")

### 子查询加载[](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#subquery-load "永久链接到这个标题")

在这种情况下，我们想表明`User.addresses`应该急切加载。加载一组对象及其相关集合的一个很好的选择是[`orm.subqueryload()`](http://docs.sqlalchemy.org/en/latest/orm/loading_relationships.html#sqlalchemy.orm.subqueryload "sqlalchemy.orm.subqueryload")选项，它会发出第二个SELECT语句，该语句完全加载与刚刚加载的结果相关联的集合。名称“子查询”源于这样一个事实，即直接通过它构造的SELECT语句[`Query`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")被重新使用，作为子查询嵌入到相关表的SELECT中。这有点精心但很容易使用：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> from sqlalchemy.orm import subqueryload
[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> jack = session.query(User).\
...                 options(subqueryload(User.addresses)).\
...                 filter_by(name='jack').one()
>>> jack
<User(name='jack', fullname='Jack Bean', password='gjffdd')>

>>> jack.addresses
[<Address(email_address='jack@google.com')>, <Address(email_address='j25@yahoo.com')>]</pre>

注意

[`subqueryload()`](http://docs.sqlalchemy.org/en/latest/orm/loading_relationships.html#sqlalchemy.orm.subqueryload "sqlalchemy.orm.subqueryload")当与限制一起使用时 [`Query.first()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.first "sqlalchemy.orm.query.Query.first")，[`Query.limit()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.limit "sqlalchemy.orm.query.Query.limit")或者[`Query.offset()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.offset "sqlalchemy.orm.query.Query.offset") 还应包括[`Query.order_by()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.order_by "sqlalchemy.orm.query.Query.order_by")在一个独特的列上，以确保正确的结果。请参阅[订购的重要性](http://docs.sqlalchemy.org/en/latest/orm/loading_relationships.html#subqueryload-ordering)。

### 加入加载[](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#joined-load "永久链接到这个标题")

另一种自动急切加载功能更为人所知并被称为 [`orm.joinedload()`](http://docs.sqlalchemy.org/en/latest/orm/loading_relationships.html#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")。这种加载方式发出JOIN，默认情况下为LEFT OUTER JOIN，因此只需一步加载主对象以及相关对象或集合。我们`addresses`以这种方式说明加载相同的 集合 - 请注意，即使实际上正在填充`User.addresses` 集合`jack`，查询也会发出额外的连接，无论如何：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> from sqlalchemy.orm import joinedload

[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> jack = session.query(User).\
...                        options(joinedload(User.addresses)).\
...                        filter_by(name='jack').one()
>>> jack
<User(name='jack', fullname='Jack Bean', password='gjffdd')>

>>> jack.addresses
[<Address(email_address='jack@google.com')>, <Address(email_address='j25@yahoo.com')>]</pre>

请注意，即使OUTER JOIN导致两行，我们仍然只有一个`User`返回实例。这是因为[`Query`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query "sqlalchemy.orm.query.Query")基于对象标识将“uniquing”策略应用于返回的实体。具体来说，可以应用联合的预先加载而不会影响查询结果。

虽然[`joinedload()`](http://docs.sqlalchemy.org/en/latest/orm/loading_relationships.html#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")已经存在了很长时间，但是[`subqueryload()`](http://docs.sqlalchemy.org/en/latest/orm/loading_relationships.html#sqlalchemy.orm.subqueryload "sqlalchemy.orm.subqueryload") 是一种新形式的渴望加载。 [`subqueryload()`](http://docs.sqlalchemy.org/en/latest/orm/loading_relationships.html#sqlalchemy.orm.subqueryload "sqlalchemy.orm.subqueryload")往往更适合加载相关集合，而[`joinedload()`](http://docs.sqlalchemy.org/en/latest/orm/loading_relationships.html#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")往往更适合多对一关系，因为只有一行加载了潜在客户和相关对象。

`joinedload()` 不是替代品 `join()`

创建的[`joinedload()`](http://docs.sqlalchemy.org/en/latest/orm/loading_relationships.html#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")联接是匿名别名，因此**不会影响查询结果**。一个[`Query.order_by()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.order_by "sqlalchemy.orm.query.Query.order_by") 或[`Query.filter()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.filter "sqlalchemy.orm.query.Query.filter")电话**无法**引用这些别名表-所谓的“用户空间”连接被利用人工 [`Query.join()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.join "sqlalchemy.orm.query.Query.join")。其基本原理[`joinedload()`](http://docs.sqlalchemy.org/en/latest/orm/loading_relationships.html#sqlalchemy.orm.joinedload "sqlalchemy.orm.joinedload")是仅应用于影响相关对象或集合作为优化细节的加载方式 - 可以添加或删除它，而不会影响实际结果。有关如何使用它的详细说明，请参阅“ [加入的渴望加载的禅](http://docs.sqlalchemy.org/en/latest/orm/loading_relationships.html#zen-of-eager-loading) ”一节。

### 明确加入+ Eagerload [](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#explicit-join-eagerload "永久链接到这个标题")

第三种类型的热切加载是当我们显式构造JOIN以便定位主行时，并且还想将额外的表应用于主对象上的相关对象或集合。此功能是通过该[`orm.contains_eager()`](http://docs.sqlalchemy.org/en/latest/orm/loading_relationships.html#sqlalchemy.orm.contains_eager "sqlalchemy.orm.contains_eager")函数提供的，最常用于在需要对同一对象进行过滤的查询上预加载多对一对象。下面我们说明加载`Address` 一行以及相关`User`对象，过滤`User`命名的“jack”并使用[`orm.contains_eager()`](http://docs.sqlalchemy.org/en/latest/orm/loading_relationships.html#sqlalchemy.orm.contains_eager "sqlalchemy.orm.contains_eager")“user”列应用于`Address.user` 属性：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> from sqlalchemy.orm import contains_eager
[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> jacks_addresses = session.query(Address).\
...                             join(Address.user).\
...                             filter(User.name=='jack').\
...                             options(contains_eager(Address.user)).\
...                             all()
>>> jacks_addresses
[<Address(email_address='jack@google.com')>, <Address(email_address='j25@yahoo.com')>]

>>> jacks_addresses[0].user
<User(name='jack', fullname='Jack Bean', password='gjffdd')></pre>

有关预先加载的更多信息，包括默认情况下如何配置各种加载形式，请参阅[关系加载技术](http://docs.sqlalchemy.org/en/latest/orm/loading_relationships.html)一节。

## 删除[](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#deleting "永久链接到这个标题")

让我们尝试删除`jack`，看看情况如何。我们将会话中的对象标记为已删除，然后我们将发出`count`查询以查看没有行保留：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> session.delete(jack)
[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> session.query(User).filter_by(name='jack').count()
0</pre>

到现在为止还挺好。杰克的`Address`物品怎么样？

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> session.query(Address).filter(
...     Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])
...  ).count()
2</pre>

哦，他们还在那里！分析刷新SQL，我们可以看到`user_id`每个地址的 列都设置为NULL，但是没有删除行。SQLAlchemy并不认为删除级联，你必须告诉它这样做。

### 配置delete / delete- [](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#configuring-delete-delete-orphan-cascade "永久链接到这个标题")

我们将在关系上配置**级联**选项`User.addresses`以更改行为。虽然SQLAlchemy允许您在任何时间点向映射添加新属性和关系，但在这种情况下需要删除现有关系，因此我们需要完全拆除映射并重新开始 - 我们将关闭[`Session`](http://docs.sqlalchemy.org/en/latest/orm/session_api.html#sqlalchemy.orm.session.Session "sqlalchemy.orm.session.Session")：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> session.close()
ROLLBACK</pre>

并使用新的[`declarative_base()`](http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/api.html#sqlalchemy.ext.declarative.declarative_base "sqlalchemy.ext.declarative.declarative_base")：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> Base = declarative_base()</pre>

接下来我们将声明`User`该类，添加`addresses`包括级联配置的关系（我们也将构造函数保留在外）：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> class User(Base):
...     __tablename__ = 'users'
...
...     id = Column(Integer, primary_key=True)
...     name = Column(String)
...     fullname = Column(String)
...     password = Column(String)
...
...     addresses = relationship("Address", back_populates='user',
...                     cascade="all, delete, delete-orphan")
...
...     def __repr__(self):
...        return "<User(name='%s', fullname='%s', password='%s')>" % (
...                                self.name, self.fullname, self.password)</pre>

然后我们重新创建`Address`，注意到在这种情况下我们已经`Address.user`通过`User`类创建了关系：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> class Address(Base):
...     __tablename__ = 'addresses'
...     id = Column(Integer, primary_key=True)
...     email_address = Column(String, nullable=False)
...     user_id = Column(Integer, ForeignKey('users.id'))
...     user = relationship("User", back_populates="addresses")
...
...     def __repr__(self):
...         return "<Address(email_address='%s')>" % self.email_address</pre>

现在，当我们加载用户时`jack`（下面使用[`get()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.get "sqlalchemy.orm.query.Query.get")，按主键加载），从相应的`addresses`集合中删除地址将导致`Address` 删除：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;"># load Jack by primary key
[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> jack = session.query(User).get(5)

# remove one Address (lazy load fires off)
[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> del jack.addresses[1]

# only one address remains
[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> session.query(Address).filter(
...     Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])
... ).count()
1</pre>

删除Jack将删除Jack以及`Address`与用户关联的其余内容：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> session.delete(jack)

[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> session.query(User).filter_by(name='jack').count()
0

[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> session.query(Address).filter(
...    Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])
... ).count()
0</pre>

更多关于瀑布

有关级联配置的更多详细信息，请参见[Cascades](http://docs.sqlalchemy.org/en/latest/orm/cascades.html#unitofwork-cascades)。级联功能还可以平滑地与关系数据库的功能集成。有关详细信息，请参阅[使用被动删除](http://docs.sqlalchemy.org/en/latest/orm/collections.html#passive-deletes)。`ON DELETE CASCADE`[](http://docs.sqlalchemy.org/en/latest/orm/collections.html#passive-deletes)

## 建立多对多的关系[](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#building-a-many-to-many-relationship "永久链接到这个标题")

我们在这里进入奖金回合，但是让我们展示一个多对多的关系。我们也会潜入其他一些功能，只是为了参观。我们将使我们的应用程序成为博客应用程序，用户可以在其中编写 `BlogPost`包含`Keyword`与之关联的项目的项目。

对于普通的多对多，我们需要创建一个未映射的[`Table`](http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")构造作为关联表。这看起来如下：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> from sqlalchemy import Table, Text
>>> # association table
>>> post_keywords = Table('post_keywords', Base.metadata,
...     Column('post_id', ForeignKey('posts.id'), primary_key=True),
...     Column('keyword_id', ForeignKey('keywords.id'), primary_key=True)
... )</pre>

在上面，我们可以看到声明a [`Table`](http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")直接与声明映射类有点不同。 [`Table`](http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")是构造函数，因此每个单独的[`Column`](http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")参数用逗号分隔。该 [`Column`](http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Column "sqlalchemy.schema.Column")对象也明确地赋予其名称，而不是从指定的属性名称中获取。

接下来，我们定义`BlogPost`并`Keyword`使用互补 [`relationship()`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")结构，每个引用`post_keywords` 表作为关联表：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> class BlogPost(Base):
...     __tablename__ = 'posts'
...
...     id = Column(Integer, primary_key=True)
...     user_id = Column(Integer, ForeignKey('users.id'))
...     headline = Column(String(255), nullable=False)
...     body = Column(Text)
...
...     # many to many BlogPost<->Keyword
...     keywords = relationship('Keyword',
...                             secondary=post_keywords,
...                             back_populates='posts')
...
...     def __init__(self, headline, body, author):
...         self.author = author
...         self.headline = headline
...         self.body = body
...
...     def __repr__(self):
...         return "BlogPost(%r, %r, %r)" % (self.headline, self.body, self.author)

>>> class Keyword(Base):
...     __tablename__ = 'keywords'
...
...     id = Column(Integer, primary_key=True)
...     keyword = Column(String(50), nullable=False, unique=True)
...     posts = relationship('BlogPost',
...                          secondary=post_keywords,
...                          back_populates='keywords')
...
...     def __init__(self, keyword):
...         self.keyword = keyword</pre>

注意

上面的类声明说明了显式`__init__()`方法。请记住，使用Declarative时，它是可选的！

以上，多对多关系是`BlogPost.keywords`。多对多关系的定义特征是`secondary`关键字参数，它引用[`Table`](http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Table "sqlalchemy.schema.Table")表示关联表的对象。该表仅包含引用关系两边的列; 如果它有*任何*其他列，例如它自己的主键，或其他表的外键，SQLAlchemy需要一个不同的使用模式，称为“关联对象”，在[关联对象中](http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#association-pattern)描述 。

我们也希望我们的`BlogPost`班级有一个`author`领域。我们将此添加为另一个双向关系，除了我们将遇到的一个问题是单个用户可能有很多博客帖子。当我们访问时 `User.posts`，我们希望能够进一步过滤结果，以免加载整个集合。为此，我们使用被[`relationship()`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship "sqlalchemy.orm.relationship")调用接受的设置`lazy='dynamic'`，该设置 在属性上配置备用**加载器策略**：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> BlogPost.author = relationship(User, back_populates="posts")
>>> User.posts = relationship(BlogPost, back_populates="author", lazy="dynamic")</pre>

创建新表：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> Base.metadata.create_all(engine)
</pre>

用法与我们一直在做的不同。让我们给Wendy一些博文：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> wendy = session.query(User).\
...                 filter_by(name='wendy').\
...                 one()
>>> post = BlogPost("Wendy's Blog Post", "This is a test", wendy)
>>> session.add(post)</pre>

我们将关键字唯一地存储在数据库中，但我们知道我们还没有，所以我们可以创建它们：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">>>> post.keywords.append(Keyword('wendy'))
>>> post.keywords.append(Keyword('firstpost'))</pre>

我们现在可以使用关键字“firstpost”查找所有博文。我们将使用 `any`运算符来查找“其中任何关键字都包含关键字字符串'firstpost'的博客帖子”：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> session.query(BlogPost).\
...             filter(BlogPost.keywords.any(keyword='firstpost')).\
...             all()
[BlogPost("Wendy's Blog Post", 'This is a test', <User(name='wendy', fullname='Wendy Williams', password='foobar')>)]</pre>

如果我们想要查找用户拥有的帖子`wendy`，我们可以告诉查询缩小到该`User`对象作为父对象：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> session.query(BlogPost).\
...             filter(BlogPost.author==wendy).\
...             filter(BlogPost.keywords.any(keyword='firstpost')).\
...             all()
[BlogPost("Wendy's Blog Post", 'This is a test', <User(name='wendy', fullname='Wendy Williams', password='foobar')>)]</pre>

或者我们可以使用Wendy自己的`posts`关系，这是一种“动态”关系，直接从那里查询：

<pre style="margin: 5px 0px; padding: 10px; font-size: 1.2em; background-color: rgb(240, 240, 240); border: 1px solid rgb(204, 204, 204); box-shadow: rgb(223, 223, 223) 2px 2px 3px; overflow: auto; line-height: 1.3em;">[SQL](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#)>>> wendy.posts.\
...         filter(BlogPost.keywords.any(keyword='firstpost')).\
...         all()
[BlogPost("Wendy's Blog Post", 'This is a test', <User(name='wendy', fullname='Wendy Williams', password='foobar')>)]</pre>

## 进一步参考[](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#further-reference "永久链接到这个标题")

查询参考：[查询API](http://docs.sqlalchemy.org/en/latest/orm/query.html)

映射器参考：[映射器配置](http://docs.sqlalchemy.org/en/latest/orm/mapper_config.html)

关系参考：[关系配置](http://docs.sqlalchemy.org/en/latest/orm/relationships.html)

会话参考：[使用会话](http://docs.sqlalchemy.org/en/latest/orm/session.html)
