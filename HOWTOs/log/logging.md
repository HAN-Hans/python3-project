# loggin HOWTOs

<!-- TOC -->

- [loggin HOWTOs](#loggin-howtos)
    - [基础日志教程](#基础日志教程)
        - [何时使用日志记录](#何时使用日志记录)
        - [一个简单的例子](#一个简单的例子)
        - [记录到文件](#记录到文件)
        - [从多个模块记录](#从多个模块记录)
        - [记录变量数据](#记录变量数据)
        - [更改显示消息的格式](#更改显示消息的格式)
        - [在消息中显示日期/时间](#在消息中显示日期时间)
        - [后续步骤](#后续步骤)
    - [高级日志教程](#高级日志教程)
        - [记录流程](#记录流程)
        - [记录器](#记录器)
        - [处理程序](#处理程序)
        - [格式化程序](#格式化程序)
        - [配置记录](#配置记录)
        - [如果没有提供配置会发生什么](#如果没有提供配置会发生什么)
        - [配置库的日志记录](#配置库的日志记录)
        - [记录级别](#记录级别)
        - [自定义级别](#自定义级别)
        - [有用的处理程序](#有用的处理程序)
        - [记录期间引发的异常](#记录期间引发的异常)
        - [使用任意对象作为消息](#使用任意对象作为消息)
        - [优化](#优化)
    - [日志cookbook](#日志cookbook)
        - [在多个模块中使用logging](#在多个模块中使用logging)
        - [从多个线程记录](#从多个线程记录)
        - [多个处理程序和格式化程序](#多个处理程序和格式化程序)
        - [记录到多个目的地](#记录到多个目的地)
        - [配置服务器示例](#配置服务器示例)
        - [处理阻止的处理程序](#处理阻止的处理程序)
        - [通过网络发送和接收日志记录事件](#通过网络发送和接收日志记录事件)
        - [将上下文信息添加到日志输出中](#将上下文信息添加到日志输出中)
        - [使用LoggerAdapters传递上下文信息](#使用loggeradapters传递上下文信息)
            - [使用除dicts之外的对象来传递上下文信息](#使用除dicts之外的对象来传递上下文信息)
            - [使用过滤器传递上下文信息](#使用过滤器传递上下文信息)
        - [从多个进程记录到单个文件](#从多个进程记录到单个文件)
        - [使用文件旋转](#使用文件旋转)
        - [使用替代格式样式](#使用替代格式样式)
        - [自定义`LogRecord`](#自定义logrecord)
        - [子类化QueueHandler - 一个ZeroMQ示例](#子类化queuehandler---一个zeromq示例)
        - [子类化QueueListener - 一个ZeroMQ示例](#子类化queuelistener---一个zeromq示例)
        - [基于字典的配置示例](#基于字典的配置示例)
        - [使用旋转器和命名器来自定义日志旋转处理](#使用旋转器和命名器来自定义日志旋转处理)
        - [更精细的多处理示例](#更精细的多处理示例)
        - [将BOM插入发送到SysLogHandler的消息中](#将bom插入发送到sysloghandler的消息中)
        - [实现结构化日志记录](#实现结构化日志记录)
        - [使用自定义处理程序](#使用自定义处理程序)
        - [在整个应用程序中使用特定格式样式](#在整个应用程序中使用特定格式样式)
            - [使用LogRecord工厂](#使用logrecord工厂)
            - [使用自定义消息对象](#使用自定义消息对象)
        - [使用配置过滤器`dictConfig()`](#使用配置过滤器dictconfig)
        - [自定义异常格式化](#自定义异常格式化)
        - [说出日志消息](#说出日志消息)
        - [缓冲日志消息并有条件地输出它们](#缓冲日志消息并有条件地输出它们)
        - [通过配置使用UTC(GMT)格式化时间](#通过配置使用utcgmt格式化时间)
        - [使用上下文管理器进行选择性记录](#使用上下文管理器进行选择性记录)

<!-- /TOC -->

---

## 基础日志教程

日志记录是一种跟踪某些软件运行时发生的事件的方法。该软件的开发人员将日志记录调用添加到其代码中，以指示已发生某些事件。通过描述性消息描述事件，该消息可以可选地包含可变数据(即，对于事件的每次出现可能不同的数据)。事件也具有开发人员对事件的重要性; 重要性也可以称为*levael* 或*severity*。

### 何时使用日志记录

日志记录为简单的日志记录使用提供了一组便利功能。这是[`debug()`](https://docs.python.org/3/library/logging.html#logging.debug "logging.debug")，[`info()`](https://docs.python.org/3/library/logging.html#logging.info "logging.info")，[`warning()`](https://docs.python.org/3/library/logging.html#logging.warning "logging.warning")，[`error()`](https://docs.python.org/3/library/logging.html#logging.error "logging.error")和[`critical()`](https://docs.python.org/3/library/logging.html#logging.critical "logging.critical")。要确定何时使用日志记录，请参阅下表，其中列出了针对一组常见任务中的每个任务的最佳工具。

| 您要执行的任务 | 这项任务的最佳工具 |
| --- | --- |
| 显示控制台输出，以便正常使用命令行脚本或程序 | [`print()`](https://docs.python.org/3/library/functions.html#print "打印") |
| 报告在程序正常运行期间发生的事件(例如，用于状态监视或故障调查) | [`logging.info()`](https://docs.python.org/3/library/logging.html#logging.info "logging.info")(或 [`logging.debug()`](https://docs.python.org/3/library/logging.html#logging.debug "logging.debug")用于诊断目的的非常详细的输出) |
| 发出有关特定运行时事件的警告 | [`warnings.warn()`](https://docs.python.org/3/library/warnings.html#warnings.warn "warnings.warn") 在库代码中，如果问题是可以避免的，则应修改客户端应用程序以消除警告  [`logging.warning()`](https://docs.python.org/3/library/logging.html#logging.warning "logging.warning") 如果客户端应用程序无法处理该情况，但仍应注意该事件 |
| 报告有关特定运行时事件的错误 | raise an exceprion |
| 报告抑制错误而不引发异常(例如，长时间运行的服务器进程中的错误处理程序) | [`logging.error()`](https://docs.python.org/3/library/logging.html#logging.error "logging.error")， [`logging.exception()`](https://docs.python.org/3/library/logging.html#logging.exception "logging.exception")或[`logging.critical()`](https://docs.python.org/3/library/logging.html#logging.critical "logging.critical")适用于特定错误和应用程序域 |

日志记录功能以它们用于跟踪的事件的级别或严重性命名。标准leval及其适用性如下所述(按严重程度递增顺序)：

| level | 什么时候使用 |
| --- | --- |
| `DEBUG` | 详细信息，通常仅在诊断问题时才有意义。 |
| `INFO` | 确认事情按预期工作。 |
| `WARNING` | 表明发生了意外情况，或表明在不久的将来出现了一些问题(例如“磁盘空间不足”)。该软件仍在按预期工作。 |
| `ERROR` | 由于更严重的问题，该软件无法执行某些功能。 |
| `CRITICAL` | 严重错误，表明程序本身可能无法继续运行。 |

默认级别为`WARNING`，这意味着将仅跟踪此级别及更高级别的事件，除非日志包已配置为执行其他操作。

可以以不同方式处理被跟踪的事件。处理跟踪事件的最简单方法是将它们打印到控制台。另一种常见方法是将它们写入磁盘文件。

### 一个简单的例子

一个非常简单的例子是：

```python
import logging
logging.warning('Watch out!')  # will print a message to the console
logging.info('I told you so')  # will not print anything
```

如果您在脚本中键入这些行并运行它，您将看到：

```
WARNING:root:Watch out!
```

打印在控制台上。由于默认级别为`WARNING`，因此不会显示`INFO`消息。打印的消息包括记录调用中提供的事件级别和描述的指示，暂时不要担心`root`部分, 稍后将对此进行解释。如果需要，可以非常灵活地格式化实际输出; 格式化选项也将在稍后解释。

### 记录到文件

一种非常常见的情况是在文件中记录日志记录事件，所以让我们看看下一步。请务必在新启动的Python解释器中尝试以下操作，并且不要只继续上述会话：

```python
import logging
logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
```

现在，如果我们打开文件并查看我们的内容，我们应该找到日志消息：

```
DEBUG:root:This message should go to the log file
INFO:root:So should this
WARNING:root:And this, too
```

此示例还说明了如何设置作为跟踪阈值的日志记录级别。在这种情况下，因为我们将阈值设置为 `DEBUG`，所以打印了所有消息。

如果要从命令行选项设置日志记录级别，例如：

```
--log=INFO
```

并且你有`--log`一些变量 *loglevel* 传递的参数的值，你可以使用：

```python
getattr(logging, loglevel.upper())
```

您将通过*level* 参数传递给[`basicConfig()`](https://docs.python.org/3/library/logging.html#logging.basicConfig "logging.basicConfig")的的时候，您可能希望对任何用户输入值进行错误检查，如下例所示：

```python
# assuming loglevel is bound to the string value obtained from the
# command line argument. Convert to upper case to allow the user to
# specify --log=DEBUG or --log=debug
numeric_level = getattr(logging, loglevel.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(level=numeric_level, ...)
```

调用[`basicConfig()`](https://docs.python.org/3/library/logging.html#logging.basicConfig "logging.basicConfig")应该在任何调用[`debug()`](https://docs.python.org/3/library/logging.html#logging.debug "logging.debug")， [`info()`](https://docs.python.org/3/library/logging.html#logging.info "logging.info")等等*之前*进行。因为它是一次性的简单配置设施，只有第一次配置后才有效后续调用实际上无效的。

如果多次运行上述脚本，则连续运行的消息将附加到文件*example.log*。如果您希望每次运行重新开始，而不记住先前运行的消息，则可以 通过将上例中的调用更改为：来指定*filemode*参数：

```python
logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)
```

输出将与之前相同，但不再附加日志文件，因此早期运行的消息将丢失。

### 从多个模块记录

如果您的程序包含多个模块，这里有一个如何组织日志记录的示例：

```python
# myapp.py
import logging
import mylib

def main():
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logging.info('Started')
    mylib.do_something()
    logging.info('Finished')

if __name__ == '__main__':
    main()
```

```python
# mylib.py
import logging

def do_something():
    logging.info('Doing something')
```

如果你运行*myapp.py*，你应该在*myapp.log*看到这个：

```
INFO:root:Started
INFO:root:Doing something
INFO:root:Finished
```

你期待看到的是什么，您可以使用*mylib.py*中的模式将应用到多个模块。请注意，这个简单的使用实例中，通过查看日志文件，除了查看事件的描述，你不会知道，在应用程序中信息的来源。如果要跟踪消息的位置，则需要参考教程级别之外的文档 - 请参阅 [高级日志教程](https://docs.python.org/3/howto/logging.html#logging-advanced-tutorial)。

### 记录变量数据

要记录变量数据，请使用格式字符串作为事件描述消息，并将变量数据作为参数附加。例如：

```python
import logging
logging.warning('%s before you %s', 'Look', 'leap!')
```

将显示：

```
WARNING:root:Look before you leap!
```

如您所见，将可变数据合并到事件描述消息中使用旧的％样式字符串格式。这是为了向后兼容：日志包提前更新的格式化选项，如 [`str.format()`](https://docs.python.org/3/library/stdtypes.html#str.format "str.format")和[`string.Template`](https://docs.python.org/3/library/string.html#string.Template "string.Template")。这些新的格式选项支持，但他们探索本教程的范围之内：看[在你的应用程序中使用特定的格式类型](https://docs.python.org/3/howto/logging-cookbook.html#formatting-styles)以获取更多信息。

### 更改显示消息的格式

要更改用于显示消息的格式，您需要指定要使用的格式：

```python
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.debug('This message should appear on the console')
logging.info('So should this')
logging.warning('And this, too')
```

那个会打印：

```
DEBUG:This message should appear on the console
INFO:So should this
WARNING:And this, too
```

请注意，前面示例中出现的“root”已消失。对于可以出现在格式字符串中的全套内容，您可以参考[LogRecord属性](https://docs.python.org/3/library/logging.html#logrecord-attributes)的文档，但是为了简单使用，您只需要*levelname*(严重性)，*message*(事件描述，包括可变数据)并可能显示当事件发生时。这将在下一节中介绍。

### 在消息中显示日期/时间

要显示事件的日期和时间，您可以在格式字符串中放置'％(asctime)s'：

```python
import logging
logging.basicConfig(format='%(asctime)s  %(message)s')
logging.warning('is when this event was logged.')
```

应该打印这样的东西：

```
2010-12-12 11:41:42,612 is when this event was logged.
```

日期/时间显示的默认格式(如上所示)类似于ISO8601或 [**RFC 3339**](https://tools.ietf.org/html/rfc3339.html)。如果您需要更多地控制日期/时间的格式，请提供 *datefmt* 参数`basicConfig`，如下例所示：

```python
import logging
logging.basicConfig(format='%(asctime)s  %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.warning('is when this event was logged.')
```

这会显示如下：

```
12/12/2010 11:46:36 AM is when this event was logged.
```

*datefmt*参数的格式与[`time.strftime()`](https://docs.python.org/3/library/time.html#time.strftime "time.strftime")支持的格式相同 。

### 后续步骤

基本教程到此结束。它应该足以让您启动并运行日志记录。日志包提供了更多功能，但为了充分利用它，您需要花费更多的时间来阅读以下部分。如果你准备好了，可以拿一些你最喜欢的饮料继续。

如果您的日志记录需求很简单，那么使用上面的示例将日志记录合并到您自己的脚本中，如果您遇到问题或者不理解某些内容，请在comp.lang.python Usenet组上发布一个问题(可从[https://groups.google.com/forum/#forum/comp.lang.python](https://groups.google.com/forum/#!forum/comp.lang.python))你应该在不久之前得到帮助。

还在？您可以继续阅读接下来的几个部分，这些部分提供了比上面基本部分更高级/深入的教程。之后，您可以查看[Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook)。

---

## 高级日志教程

日志库采用模块化方法，并提供几类组件：`Logger`(记录器)，`Handler`(处理程序)，`Filter`(过滤器)和`Formatter`(格式化程序)。

* Loggers记录器公开应用程序代码直接使用的接口。
* Handlers处理程序将日志记录(由记录器创建)发送到适当的目标。
* Filters过滤器提供了更精细的设施，用于确定要输出的日志记录。
* Formatters指定最终输出中的日志记录的布局。

日志事件信息在`LogRecod`实例中的记录器，处理程序，过滤器和格式化程序之间传递。

通过在[`Logger`](https://docs.python.org/3/library/logging.html#logging.Logger "logging.Logger") 类的实例上调用方法(以下称为 *logger* )来执行日志记录。每个实例都有一个名称，它们在概念上以点(句点)作为分隔符排列在命名空间层次结构中。例如，名为'scan'的记录器是记录器'scan.text'，'scan.html'和'scan.pdf'的父级。记录器名称可以是您想要的任何名称，并指示记录消息源自的应用程序区域。

在命名记录器时使用的一个好习惯是在每个使用日志记录的模块中使用模块级记录器，命名如下：

```python
logger = logging.getLogger(__name__)
```

这意味着记录器名称跟踪包/模块层次结构，并且直观地显示从记录器名称记录事件的位置。

记录器层次结构的根称为根记录器。这是由函数使用的记录[`debug()`](https://docs.python.org/3/library/logging.html#logging.debug "logging.debug")，[`info()`](https://docs.python.org/3/library/logging.html#logging.info "logging.info")，[`warning()`](https://docs.python.org/3/library/logging.html#logging.warning "logging.warning")， [`error()`](https://docs.python.org/3/library/logging.html#logging.error "logging.error")和[`critical()`](https://docs.python.org/3/library/logging.html#logging.critical "logging.critical")，这只是调用根记录的同名方法。功能和方法具有相同的签名。根记录器的名称在记录的输出中打印为“root”。

当然，可以将消息记录到不同的目的地。logging包中包含支持: 用于将日志消息写入文件，HTTP GET/POST位置，通过SMTP发送电子邮件，通用套接字，队列或特定于操作系统的日志记录机制(如syslog或Windows NT事件日志)。目标由`handler`类提供。如果您有任何内置处理程序类未满足的特殊要求，则可以创建自己的日志目标类。

默认情况下，没有为任何日志记录消息设置目标。您可以使用[`basicConfig()`](https://docs.python.org/3/library/logging.html#logging.basicConfig "logging.basicConfig")教程示例中的as指定目标(例如控制台或文件)。如果你调用的函数 [`debug()`](https://docs.python.org/3/library/logging.html#logging.debug "logging.debug")，[`info()`](https://docs.python.org/3/library/logging.html#logging.info "logging.info")， [`warning()`](https://docs.python.org/3/library/logging.html#logging.warning "logging.warning")，[`error()`](https://docs.python.org/3/library/logging.html#logging.error "logging.error")和[`critical()`](https://docs.python.org/3/library/logging.html#logging.critical "logging.critical")，他们会检查，看看是否未设置目标; 如果未设置，则`sys.stderr`在委派给根记录器执行实际消息输出之前，他们将设置console()的目标和显示消息的默认格式。

[`basicConfig()`](https://docs.python.org/3/library/logging.html#logging.basicConfig "logging.basicConfig")消息设置的默认格式为：

```
severity:logger name:message
```

您可以通过[`basicConfig()`](https://docs.python.org/3/library/logging.html#logging.basicConfig "logging.basicConfig")使用 *format*关键字参数传递格式字符串来更改此设置。有关如何构造格式字符串的所有选项，请参阅[格式化对象](https://docs.python.org/3/library/logging.html#formatter-objects)。

### 记录流程

记录器和处理程序中的日志事件信息流程如下图所示。

![../_images/logging_flow.png](http://upload-images.jianshu.io/upload_images/13148580-771353f5d280b926.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 记录器

[`Logger`](https://docs.python.org/3/library/logging.html#logging.Logger "logging.Logger")对象有三重的作用。首先，它们向应用程序代码公开了几种方法，以便应用程序可以在运行时记录消息 其次，记录器对象根据严重性(默认过滤工具)或过滤器对象确定要处理的日志消息。第三，记录器对象将相关的日志消息传递给所有感兴趣的日志处理程序。

记录器对象上使用最广泛的方法分为两类：配置和消息发送。

这些是最常见的配置方法：

* [`Logger.setLevel()`](https://docs.python.org/3/library/logging.html#logging.Logger.setLevel "logging.Logger.setLevel")指定记录器将处理的最低严重性日志消息，其中debug是最低内置严重性级别，critical是最高内置严重性级别。例如，如果严重性级别为INFO，则记录器将仅处理INFO，WARNING，ERROR和CRITICAL消息，并将忽略DEBUG消息。
* [`Logger.addHandler()`](https://docs.python.org/3/library/logging.html#logging.Logger.addHandler "logging.Logger.addHandler")和[`Logger.removeHandler()`](https://docs.python.org/3/library/logging.html#logging.Logger.removeHandler "logging.Logger.removeHandler")从logger对象添加和删除处理程序对象。处理程序中详细介绍了[Handlers](https://docs.python.org/3/howto/logging.html#handler-basic)。
* [`Logger.addFilter()`](https://docs.python.org/3/library/logging.html#logging.Logger.addFilter "logging.Logger.addFilter")和[`Logger.removeFilter()`](https://docs.python.org/3/library/logging.html#logging.Logger.removeFilter "logging.Logger.removeFilter")从记录器对象中添加和删除过滤器对象。过滤器对象中详细介绍了[Filtters](https://docs.python.org/3/library/logging.html#filter)。

您不需要始终在您创建的每个记录器上调用这些方法。请参阅本节的最后两段。

配置logger对象后，以下方法将创建日志消息：

* [`Logger.debug()`](https://docs.python.org/3/library/logging.html#logging.Logger.debug "logging.Logger.debug")，[`Logger.info()`](https://docs.python.org/3/library/logging.html#logging.Logger.info "logging.Logger.info")，[`Logger.warning()`](https://docs.python.org/3/library/logging.html#logging.Logger.warning "logging.Logger.warning")， [`Logger.error()`](https://docs.python.org/3/library/logging.html#logging.Logger.error "logging.Logger.error")，和[`Logger.critical()`](https://docs.python.org/3/library/logging.html#logging.Logger.critical "logging.Logger.critical")所有的消息，并对应各自的方法名称的级别创建日志记录。该消息实际上是一个格式串，其可以包含的标准字符串替换语法`%s`，`%d`，`%f`，等。其余参数是与消息中的替换字段对应的对象列表。关于`**kwargs`，日志记录方法仅关注关键字，`exc_info`并使用它来确定是否记录异常信息。
* [`Logger.exception()`](https://docs.python.org/3/library/logging.html#logging.Logger.exception "logging.Logger.exception")创建类似于的日志消息 [`Logger.error()`](https://docs.python.org/3/library/logging.html#logging.Logger.error "logging.Logger.error")。不同之处在于[`Logger.exception()`](https://docs.python.org/3/library/logging.html#logging.Logger.exception "logging.Logger.exception")转储堆栈跟踪。仅从异常处理程序调用此方法。
* [`Logger.log()`](https://docs.python.org/3/library/logging.html#logging.Logger.log "logging.Logger.log")将日志级别作为显式参数。对于记录消息而言，这比使用上面列出的日志级别便捷方法要详细一些，但这是如何记录自定义日志级别。

[`getLogger()`](https://docs.python.org/3/library/logging.html#logging.getLogger "logging.getLogger")如果提供了指定名称，则返回对具有指定名称的记录器实例的引用，否则返回`root`。名称是以`.`(点号)分隔层次结构，[`getLogger()`](https://docs.python.org/3/library/logging.html#logging.getLogger "logging.getLogger")具有相同名称的多次调用将返回对同一记录器对象的引用，在分层列表中较低的记录器是列表中较高的记录器的子项。例如，给定一个记录器使用的名称`foo`，记录仪用的名字 `foo.bar`，`foo.bar.baz`以及`foo.bam`是所有后代`foo`。

记录器具有*有效级别*的概念。如果未在记录器上显式设置级别，则使用其父级别作为其有效级别。如果父记录器也没有明确的级别设置，则检查祖先记录器，直到搜索明确设置级别的祖先记录器被发现。根记录器始终具有显式级别集(`WARNING`默认情况下)。在决定是否处理事件时，记录器的有效级别用于确定事件是否传递给记录器的处理程序。

子记录器将消息传播到与其祖先记录器相关联的处理程序。因此，不必为应用程序使用的所有记录器定义和配置处理程序。为顶级记录器配置处理程序并根据需要创建子记录器就足够了。(但是，您可以通过将 记录器的*propagate*属性设置为`False`来关闭传播。)

### 处理程序

[`Handler`](https://docs.python.org/3/library/logging.html#logging.Handler "logging.Handler")对象负责将适当的日志消息(基于日志消息的严重性)分派给处理程序的指定目标。 [`Logger`](https://docs.python.org/3/library/logging.html#logging.Logger "logging.Logger")对象可以使用[`addHandler()`](https://docs.python.org/3/library/logging.html#logging.Logger.addHandler "logging.Logger.addHandler")方法向自己添加零个或多个处理程序对象。作为示例场景，应用程序可能希望将所有日志消息发送到日志文件，将错误或更高的所有日志消息发送到标准输出，以及对至关重要的所有消息发送电子邮件。此方案需要三个单独的处理程序，其中每个处理程序负责将特定严重性的消息发送到特定位置。

标准库包含很多处理程序类型(请参阅 [有用的处理程序](https://docs.python.org/3/howto/logging.html#useful-handlers))，教程主要使用[`StreamHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.StreamHandler "logging.StreamHandler")和[`FileHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.FileHandler "logging.FileHandler")在其示例中使用。

处理程序中很少有方法可供应用程序开发人员关注，与使用内置处理程序对象(即不创建自定义处理程序)的应用程序开发人员相关的唯一处理程序方法是以下配置方法：

* 该[`setLevel()`](https://docs.python.org/3/library/logging.html#logging.Handler.setLevel "logging.Handler.setLevel")方法与logger对象一样，指定将分派到适当目标的最低严重性。为什么有两种`setLevel()`方法？记录器中设置的级别确定将传递给其处理程序的消息的严重性。每个处理程序中设置的级别确定处理程序将发送哪些消息。
* [`setFormatter()`](https://docs.python.org/3/library/logging.html#logging.Handler.setFormatter "logging.Handler.setFormatter") 选择要使用的此处理程序的Formatter对象。
* [`addFilter()`](https://docs.python.org/3/library/logging.html#logging.Handler.addFilter "logging.Handler.addFilter")并[`removeFilter()`](https://docs.python.org/3/library/logging.html#logging.Handler.removeFilter "logging.Handler.removeFilter")分别在处理程序上配置和取消配置过滤器对象。

应用程序代码不应直接实例化和使用实例 [`Handler`](https://docs.python.org/3/library/logging.html#logging.Handler "logging.Handler")。相反，[`Handler`](https://docs.python.org/3/library/logging.html#logging.Handler "logging.Handler")该类是一个基类，它定义了所有处理程序应具有的接口，并建立了子类可以使用(或覆盖)的一些默认行为。

### 格式化程序

Formatter对象配置日志消息的最终顺序，结构和内容。与基[`logging.Handler`](https://docs.python.org/3/library/logging.html#logging.Handler "logging.Handler")类不同，应用程序代码可以实例化格式化程序类，但如果应用程序需要特殊行为，则可能会对格式化程序进行子类化。构造函数有三个可选参数 - 消息格式字符串，日期格式字符串和样式指示符。

```python
logging.Formatter.__init__(fmt=None，datefmt=None，style='％')
```

如果没有消息格式字符串，则默认使用原始消息。如果没有日期格式字符串，则默认日期格式为：

```
%Y-%m-%d %H:%M:%S
```

`style`是'％', '{'或'$'之一。如果未指定其中一个，则使用'％'。

如果`style`是'％'，则消息格式字符串使用`%(<dictionary key>)s`[](https://docs.python.org/3/library/logging.html#logrecord-attributes)样式字符串替换; [LogRecord属性](https://docs.python.org/3/library/logging.html#logrecord-attributes)中记录了可能的键。如果样式为“{”，则假定消息格式字符串与[`str.format()`](https://docs.python.org/3/library/stdtypes.html#str.format "str.format")(使用关键字参数)兼容，而如果样式为'$'，则消息格式字符串应符合预期的[`string.Template.substitute()`](https://docs.python.org/3/library/string.html#string.Template.substitute "string.Template.substitute")格式。

版本3.2中已更改：添加了`style`参数。

以下消息格式字符串将按以下顺序以人类可读的格式记录时间，消息的严重性和消息的内容：

```python
'%(asctime)s - %(levelname)s - %(message)s'
```

Formatters使用用户可配置的函数将记录的创建时间转换为元组。默认[`time.localtime()`](https://docs.python.org/3/library/time.html#time.localtime "time.localtime")使用; 要为特定格式化程序实例更改此设置，请将实例的`converter`属性设置为具有与[`time.localtime()`](https://docs.python.org/3/library/time.html#time.localtime "time.localtime")或 相同签名的函数[`time.gmtime()`](https://docs.python.org/3/library/time.html#time.gmtime "time.gmtime")。要为所有格式化程序更改它，例如，如果您希望所有日志记录时间都以GMT `converter`格式`time.gmtime`显示，请在Formatter类中设置该属性(以用于GMT显示)。

### 配置记录

程序员可以通过三种方式配置日志记录：

1. 使用调用上面列出的配置方法的Python代码显式创建记录器，处理程序和格式化程序。
2. 创建日志配置文件并使用该[`fileConfig()`](https://docs.python.org/3/library/logging.config.html#logging.config.fileConfig "logging.config.fileConfig") 函数读取它。
3. 创建配置信息字典并将其传递给[`dictConfig()`](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig "logging.config.dictConfig")函数。

有关最后两个选项的参考文档，请参阅 [配置功能](https://docs.python.org/3/library/logging.config.html#logging-config-api)。以下示例使用Python代码配置一个非常简单的记录器，一个控制台处理程序和一个简单的格式化程序：

```python
import logging

# create logger
logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')
```

从命令行运行此模块将生成以下输出：

```sh
$ python simple_logging_module.py
2005-03-19 15:10:26,618 - simple_example - DEBUG - debug message
2005-03-19 15:10:26,620 - simple_example - INFO - info message
2005-03-19 15:10:26,695 - simple_example - WARNING - warn message
2005-03-19 15:10:26,697 - simple_example - ERROR - error message
2005-03-19 15:10:26,773 - simple_example - CRITICAL - critical message
```

以下Python模块创建的记录器，处理程序和格式化程序与上面列出的示例几乎完全相同，唯一的区别是对象的名称：

```python
import logging
import logging.config

logging.config.fileConfig('logging.conf')

# create logger
logger = logging.getLogger('simpleExample')

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')
```

这是logging.conf文件：

```python
[loggers]
keys=root,simpleExample

[handlers]
keys=consoleHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_simpleExample]
level=DEBUG
handlers=consoleHandler
qualname=simpleExample
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout,)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=
```

输出几乎与基于非配置文件的示例相同：

```sh
$ python simple_logging_config.py
2005-03-19 15:38:55,977 - simpleExample - DEBUG - debug message
2005-03-19 15:38:55,979 - simpleExample - INFO - info message
2005-03-19 15:38:56,054 - simpleExample - WARNING - warn message
2005-03-19 15:38:56,055 - simpleExample - ERROR - error message
2005-03-19 15:38:56,130 - simpleExample - CRITICAL - critical message
```

您可以看到配置文件方法与Python代码方法相比具有一些优势，主要是配置和代码的分离以及非编码器轻松修改日志记录属性的能力。

**警告:**

该[`fileConfig()`](https://docs.python.org/3/library/logging.config.html#logging.config.fileConfig "logging.config.fileConfig")函数采用默认参数， `disable_existing_loggers`默认`True`为出于向后兼容的原因。这可能是您想要的，也可能不是，因为[`fileConfig()`](https://docs.python.org/3/library/logging.config.html#logging.config.fileConfig "logging.config.fileConfig")除非在配置中明确命名它们(或祖先)，否则它将导致在调用之前存在的任何记录器被禁用。有关更多信息，请参阅参考文档，`False`如果需要，请指定此参数。

传递给的字典[`dictConfig()`](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig "logging.config.dictConfig")也可以使用键指定布尔值`disable_existing_loggers`，如果未在字典中明确指定，则默认为解释为 `True`。这会导致上面描述的记录器禁用行为，这可能不是您想要的 - 在这种情况下，明确地为键提供值`False`。

请注意，配置文件中引用的类名称需要相对于日志记录模块，或者可以使用常规导入机制解析的绝对值。因此，您可以使用 [`WatchedFileHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.WatchedFileHandler "logging.handlers.WatchedFileHandler")(相对于日志记录模块)或 `mypackage.mymodule.MyHandler`(对于在包`mypackage` 和模块中定义的类`mymodule`，在`mypackage`Python导入路径上可用的位置)。

在Python 3.2中，引入了一种新的配置日志记录的方法，使用字典来保存配置信息。这提供了上面概述的基于配置文件的方法的功能的超集，并且是新应用程序和部署的推荐配置方法。因为Python字典用于保存配置信息，并且由于您可以使用不同的方式填充该字典，因此您有更多的配置选项。例如，您可以使用JSON格式的配置文件，或者，如果您有权访问YAML处理功能，则可以使用YAML格式的文件来填充配置字典。或者，当然，您可以在Python代码中构建字典，通过套接字以pickle形式接收它，或者使用对您的应用程序有意义的任何方法。

以下是与上述相同配置的示例，采用YAML格式，用于新的基于字典的方法：

```python
version: 1
formatters:
  simple:
    format: '%(asctime)s  -  %(name)s  -  %(levelname)s  -  %(message)s'
handlers:
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: simple
    stream: ext://sys.stdout
loggers:
  simpleExample:
    level: DEBUG
    handlers: [console]
    propagate: no
root:
  level: DEBUG
  handlers: [console]
```

有关使用字典进行日志记录的详细信息，请参阅 [配置功能](https://docs.python.org/3/library/logging.config.html#logging-config-api)。

### 如果没有提供配置会发生什么

如果未提供日志记录配置，则可能出现需要输出日志记录事件但无法找到输出事件的处理程序的情况。在这些情况下，日志包的行为取决于Python版本。

对于3.2之前的Python版本，行为如下：

* 如果*logging.raiseExceptions*是`False`(生产模式)，则会以静默方式删除该事件。
* 如果*logging.raiseExceptions*是`True`(开发模式)，则会打印一条消息“无法找到记录器XYZ的处理程序”。

在Python 3.2及更高版本中，行为如下：

* 该事件使用“最后的处理程序”输出，存储在 `logging.lastResort`。此内部处理程序不与任何记录器关联，其作用类似于[`StreamHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.StreamHandler "logging.StreamHandler")将事件描述消息写入当前值`sys.stderr`(因此尊重可能有效的任何重定向)。没有对消息进行格式化 - 只打印裸事件描述消息。处理程序的级别设置为`WARNING`，因此将输出此级别和更高级别的所有事件。

要获得3.2之前的行为，`logging.lastResort`可以设置为`None`。

### 配置库的日志记录

在开发使用日志记录的python库时，您应该注意python库如何使用日志记录 - 例如，使用的记录器的名称。还需要考虑其日志记录配置。如果应用程序中不使用loggging，但是库代码进行日志记录调用，则(如上一节所述)将打印严重性`WARNING`和更高级别的事件 到`sys.stderr`。这被认为是最好的默认行为。

如果由于某种原因您不希望在没有任何日志记录配置的情况下打印这些消息，则可以将无操作处理程序附加到库的顶级记录器。这样可以避免打印消息，因为将始终为库的事件找到处理程序：它不会产生任何输出。如果库用户配置日志以供应用程序使用，可能会在配置中添加一些处理程序，并且级别，则在库代码中进行的日志记录调用将正常地将输出发送给这些处理程序。

日志包中包含一个do-nothing处理程序( [`NullHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.NullHandler "logging.NullHandler")自Python 3.1起)。可以将此处理程序的实例添加到库使用的日志记录命名空间的顶级记录器中(如果要`sys.stderr`在没有日志记录配置的情况下阻止将库的记录事件输出到 )。如果库*foo的*所有日志记录都是使用名称匹配'foo.x'，'foo.x.y'等的记录器完成的，那么代码：

```python
import logging
logging.getLogger('foo').addHandler(logging.NullHandler())
```

应该有所期望的效果。如果组织生成了许多库，则指定的记录器名称可以是“orgname.foo”而不仅仅是“foo”。

**注意:**

强烈建议您不要在你的library's loggers添加 *NullHandler* 之外任何处理程序。这是因为处理程序的配置是使用您的库的应用程序开发人员的特权。应用程序开发人员了解他们的目标受众以及哪些处理程序最适合他们的应用程序：如果您在“引擎盖下”添加处理程序，则可能会干扰他们执行单元测试和提供符合其要求的日志的能力。

### 记录级别

日志记录级别的数值在下表中给出。如果要定义自己的级别，并且需要它们具有相对于预定义级别的特定值，则主要关注这些级别。如果您使用相同的数值定义级别，它将覆盖预定义的值; 预定义的名称丢失。

| leval | 数值 |
| --- | --- |
| `CRITICAL` | 50 |
| `ERROR` | 40 |
| `WARNING` | 30 |
| `INFO` | 20 |
| `DEBUG` | 10 |
| `NOTSET` | 0 |

级别也可以与记录器相关联，由开发人员或通过加载已保存的日志记录配置来设置。在记录器上调用日志记录方法时，记录器会将其自身级别与与方法调用关联的级别进行比较。如果记录器的级别高于方法调用的级别，则实际上不会生成任何记录消息。这是控制日志输出详细程度的基本机制。

记录消息被编码为`LogRecord`类的实例。当记录器决定实际记录事件时， `LogRecod`将从记录消息创建实例。

记录消息通过使用 *handler* 调度机制，是*Handler*类的子类的实例。处理程序负责确保记录的消息(以a的形式`LogRecod`)最终位于特定位置(或一组位置)，这对该消息的目标受众有用(例如最终用户，支持服务台员工，系统管理员，开发商)。处理程序是`LogRecod`为特定目标传递的实例。每个记录器可以有零个，一个或多个与之关联的处理程序(通过 [`addHandler()`](https://docs.python.org/3/library/logging.html#logging.Logger.addHandler "logging.Logger.addHandler")方法[`Logger`](https://docs.python.org/3/library/logging.html#logging.Logger "logging.Logger"))。除了与记录器直接关联的任何处理程序之外，还会调用*与记录器的所有祖先关联的所有处理程序*来分派消息(除非记录器的*propagate(传播)*标志设置为false值，此时传递给祖先处理程序停止)。

就像记录器一样，处理程序可以具有与它们相关联的级别。处理程序的级别充当过滤器，其方式与记录器级别相同。如果处理程序决定实际调度事件，则该[`emit()`](https://docs.python.org/3/library/logging.html#logging.Handler.emit "logging.Handler.emit")方法用于将消息发送到其目标。大多数用户定义的子类[`Handler`](https://docs.python.org/3/library/logging.html#logging.Handler "logging.Handler")都需要覆盖它[`emit()`](https://docs.python.org/3/library/logging.html#logging.Handler.emit "logging.Handler.emit")。

### 自定义级别

你可以定义自己的leval，但不一定是必要的，因为现有leval是根据实践经验选择的。但是，如果您确信需要自定义级别，则在执行此操作时应特别小心，*如果您正在开发库，则定义自定义级别*可能是*一个非常糟糕的主意*。这是因为如果多个库作者都定义了他们自己的自定义级别，那么使用开发人员很难控制和/或解释这些多个库的日志记录输出，因为给定的数值可能意味着不同的东西对于不同的图书馆

### 有用的处理程序

除了基[`Handler`](https://docs.python.org/3/library/logging.html#logging.Handler "logging.Handler")类之外，还提供了许多有用的子类：

1. [`StreamHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.StreamHandler "logging.StreamHandler") 实例将消息发送到流(类文件对象)。
2. [`FileHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.FileHandler "logging.FileHandler") 实例将消息发送到磁盘文件。
3. [`BaseRotatingHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.BaseRotatingHandler "logging.handlers.BaseRotatingHandler")是在某个点旋转日志文件的处理程序的基类。它并不意味着直接实例化。相反，使用`RotatingFileHandler`或 `TimedRotatingFileHandler`
4. [`RotatingFileHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.RotatingFileHandler "logging.handlers.RotatingFileHandler") 实例将消息发送到磁盘文件，支持最大日志文件大小和日志文件轮换。
5. [`TimedRotatingFileHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.TimedRotatingFileHandler "logging.handlers.TimedRotatingFileHandler") 实例将消息发送到磁盘文件，以特定的时间间隔旋转日志文件。
6. [`SocketHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.SocketHandler "logging.handlers.SocketHandler")实例将消息发送到TCP / IP套接字。从3.4开始，也支持Unix域套接字。
7. [`DatagramHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.DatagramHandler "logging.handlers.DatagramHandler")实例将消息发送到UDP套接字。从3.4开始，也支持Unix域套接字。
8. [`SMTPHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.SMTPHandler "logging.handlers.SMTPHandler") 实例将消息发送到指定的电子邮件地址。
9. [`SysLogHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.SysLogHandler "logging.handlers.SysLogHandler") 实例将消息发送到Unix syslog守护程序，可能在远程计算机上。
10. [`NTEventLogHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.NTEventLogHandler "logging.handlers.NTEventLogHandler") 实例将消息发送到Windows NT / 2000 / XP事件日志。
11. [`MemoryHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.MemoryHandler "logging.handlers.MemoryHandler") 实例将消息发送到内存中的缓冲区，只要满足特定条件，就会刷新。
12. [`HTTPHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.HTTPHandler "logging.handlers.HTTPHandler")实例使用任一语义`GET`或`POST`语义将消息发送到HTTP服务器。
13. [`WatchedFileHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.WatchedFileHandler "logging.handlers.WatchedFileHandler")实例会监视他们要登录的文件。如果文件发生更改，则会关闭该文件并使用文件名重新打开。此处理程序仅在类Unix系统上有用; Windows不支持使用的基础机制。
14. [`QueueHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.QueueHandler "logging.handlers.QueueHandler")实例将消息发送到队列，例如在[`queue`](https://docs.python.org/3/library/queue.html#module-queue "queue：同步的队列类。")或[`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing "多处理：基于进程的并行性。")模块中实现的那些队列。
15. [`NullHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.NullHandler "logging.NullHandler")实例不执行任何错误消息。它们由想要使用日志记录的库开发人员使用，但是希望避免“如果库用户未配置日志记录，则可以显示”没有找到记录器XXX的处理程序“消息。有关更多信息，请参阅[配置库的日志记录](https://docs.python.org/3/howto/logging.html#library-config)。

新的3.1版：的`NullHandler`类。

新版本3.2：在`QueueHandler`类。

`NullHandler`，`StreamHandler`和`FileHandler`类在核心日志包中定义。其他处理程序在子模块中定义[`logging.handlers`](https://docs.python.org/3/library/logging.handlers.html#module-logging.handlers "logging.handlers：日志记录模块的处理程序。")。(还有另一个子模块[`logging.config`](https://docs.python.org/3/library/logging.config.html#module-logging.config "logging.config：日志记录模块的配置。")，用于配置功能。)

记录的消息被格式化以便通过`Formatter`类的实例进行呈现 。它们使用适合与％运算符和字典一起使用的格式字符串进行初始化。

对于批量格式化多个消息，`BufferingFormatter`可以使用实例 。除了格式字符串(应用于批处理中的每个消息)之外，还提供了标题和尾部格式字符串。

当基于记录器级和/或处理过滤leval是不够的，的实例[`Filter`](https://docs.python.org/3/library/logging.html#logging.Filter "logging.Filter")可以被添加到[`Logger`](https://docs.python.org/3/library/logging.html#logging.Logger "logging.Logger")和 [`Handler`](https://docs.python.org/3/library/logging.html#logging.Handler "logging.Handler")实例(通过他们的`addFilter()`方法)。在决定进一步处理消息之前，记录器和处理程序都会查询其所有过滤器以获取权限。如果任何过滤器返回false值，则不会进一步处理该消息。

基本[`Filter`](https://docs.python.org/3/library/logging.html#logging.Filter "logging.Filter")功能允许按特定记录器名称进行过滤。如果使用此功能，则允许通过过滤器发送到指定记录器及其子项的消息，并删除所有其他消息。

### 记录期间引发的异常

日志包旨在吞噬登录生产时发生的异常。这样，处理日志记录事件时发生的错误(例如记录错误配置，网络或其他类似错误)不会导致使用日志记录的应用程序过早终止。

[`SystemExit`](https://docs.python.org/3/library/exceptions.html#SystemExit "SystemExit")和[`KeyboardInterrupt`](https://docs.python.org/3/library/exceptions.html#KeyboardInterrupt "一个KeyboardInterrupt")异常从未吞噬。在子类[`emit()`](https://docs.python.org/3/library/logging.html#logging.Handler.emit "logging.Handler.emit")方法期间发生的其他异常[`Handler`](https://docs.python.org/3/library/logging.html#logging.Handler "logging.Handler")将传递给其[`handleError()`](https://docs.python.org/3/library/logging.html#logging.Handler.handleError "logging.Handler.handleError") 方法。

`handleError()`in `Handler` 检查的默认实现，以查看是否设置了模块级变量`raiseExceptions`。如果设置，则打印回溯`sys.stderr`。如果未设置，则吞下异常。

注意

默认值`raiseExceptions`是`True`。这是因为在开发期间，您通常希望收到发生的任何异常的通知。它建议您设置`raiseExceptions`到 `False`用于生产使用。

### 使用任意对象作为消息

在前面的部分和示例中，假设记录事件时传递的消息是字符串。但是，这不是唯一的可能性。您可以将任意对象作为消息传递，并且当日志记录系统需要将其转换为字符串表示时，将调用其`__str__()`方法。事实上，如果你愿意，你可以避免完全计算字符串表示 - 例如，`SocketHandler`通过pickle并通过线路发送事件来发出事件。

### 优化

消息参数的格式化将被推迟，直到无法避免。但是，计算传递给日志记录方法的参数也可能很昂贵，如果记录器只是丢弃您的事件，您可能希望避免这样做。要决定做什么，可以调用带有level参数的[`isEnabledFor()`](https://docs.python.org/3/library/logging.html#logging.Logger.isEnabledFor "logging.Logger.isEnabledFor")方法，如果Logger为该级别的调用创建了事件，则返回true。你可以写这样的代码：

```python
if logger.isEnabledFor(logging.DEBUG):
    logger.debug('Message with %s, %s', expensive_func1(),
                                        expensive_func2())
```

因此，如果记录器的阈值设置在上面`DEBUG`，则调用`expensive_func1()`和`expensive_func2()`从不进行调用。

**注意:**

在某些情况下，`isEnabledFor()`本身可能比您想要的更昂贵(例如，对于深度嵌套的记录器，其中显式级别仅在记录器层次结构中设置为高)。在这种情况下(或者如果您想避免在紧密循环中调用方法)，您可以将调用的结果缓存到`isEnabledFor()`本地或实例变量中，并使用它而不是每次都调用该方法。当日志记录配置在应用程序运行时动态更改(这不常见)时，只需要重新计算这样的缓存值。

还可以针对特定应用程序进行其他优化，这些应用程序需要更精确地控制收集的日志记录信息。以下是您可以执行的操作列表，以避免在您不需要的日志记录期间进行处理：

| 你不想收集什么 | 如何避免收集它 |
| --- | --- |
| 有关信息的来源和调用 | 设置`logging._srcfile`为`None`。这样可以避免调用`sys._getframe()`，`sys._getframe()`如果PyPy支持Python 3.x ，这可能有助于加速PyPy(无法加速使用的代码)等环境中的代码。 |
| 线程信息 | 设置`logging.logThreads`为`0`。 |
| 处理信息 | 设置`logging.logProcesses`为`0`。 |

另请注意，核心日志记录模块仅包含基本处理程序。如果您不导入[  `logging.handlers`](https://docs.python.org/3/library/logging.handlers.html#module-logging.handlers "logging.handlers：日志记录模块的处理程序。")和[`logging.config`](https://docs.python.org/3/library/logging.config.html#module-logging.config "logging.config：日志记录模块的配置。")，就不会占用任何内存。

---

## 日志cookbook

[日志cookbook](https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook "永久链接到这个标题")此页面包含许多与日志记录相关的配方，这些配方过去一直很有用。

### 在多个模块中使用logging

多次调用以`logging.getLogger('someLogger')`返回对同一记录器对象的引用。这不仅在同一模块中，而且在模块之间也是如此，只要它在同一个Python解释器过程中。引用同一个对象是正确的; 此外，应用程序代码可以在一个模块中定义和配置父记录器，并在单独的模块中创建(但不配置)子记录器，并且对子项的所有记录器调用都将传递给父项。这是一个主要 main 模块：

```python
import logging
import auxiliary_module

# create logger with 'spam_application'
logger = logging.getLogger('spam_application')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('spam.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.info('creating an instance of auxiliary_module.Auxiliary')
a = auxiliary_module.Auxiliary()
logger.info('created an instance of auxiliary_module.Auxiliary')
logger.info('calling auxiliary_module.Auxiliary.do_something')
a.do_something()
logger.info('finished auxiliary_module.Auxiliary.do_something')
logger.info('calling auxiliary_module.some_function()')
auxiliary_module.some_function()
logger.info('done with auxiliary_module.some_function()')
```

这是辅助 auxiliary 模块：

```python
import logging

# create logger
module_logger = logging.getLogger('spam_application.auxiliary')

class Auxiliary:
    def __init__(self):
        self.logger = logging.getLogger('spam_application.auxiliary.Auxiliary')
        self.logger.info('creating an instance of Auxiliary')

    def do_something(self):
        self.logger.info('doing something')
        a = 1 + 1
        self.logger.info('done doing something')

def some_function():
    module_logger.info('received a call to "some_function"')
```

输出如下：

```
2018-09-23 15:57:30,687 - spam_application - INFO - creating an instance of auxiliary_module.Auxiliary
2018-09-23 15:57:30,687 - spam_application.auxiliary.Auxiliary - INFO - creating an instance of Auxiliary
2018-09-23 15:57:30,687 - spam_application - INFO - created an instance of auxiliary_module.Auxiliary
2018-09-23 15:57:30,687 - spam_application - INFO - calling auxiliary_module.Auxiliary.do_something
2018-09-23 15:57:30,687 - spam_application.auxiliary.Auxiliary - INFO - doing something
2018-09-23 15:57:30,687 - spam_application.auxiliary.Auxiliary - INFO - done doing something
2018-09-23 15:57:30,687 - spam_application - INFO - finished auxiliary_module.Auxiliary.do_something
2018-09-23 15:57:30,687 - spam_application - INFO - calling auxiliary_module.some_function()
2018-09-23 15:57:30,687 - spam_application.auxiliary - INFO - received a call to "some_function"
2018-09-23 15:57:30,687 - spam_application - INFO - done with auxiliary_module.some_function()
```

### 从多个线程记录

从多个线程进行日志记录不需要特别的技巧。以下示例显示了从主(初始)线程和另一个线程进行的日志记录：

```python
import logging
import threading
import time

def worker(arg):
    while not arg['stop']:
        logging.debug('Hi from myfunc')
        time.sleep(0.5)

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d  %(threadName)s  %(message)s')
    info = {'stop': False}
    thread = threading.Thread(target=worker, args=(info,))
    thread.start()
    while True:
        try:
            logging.debug('Hello from main')
            time.sleep(0.75)
        except KeyboardInterrupt:
            info['stop'] = True
            break
    thread.join()

if __name__ == '__main__':
    main()
```

运行时，脚本应该打印如下内容：

```
   0 Thread-1 Hi from myfunc
   3 MainThread Hello from main
 505 Thread-1 Hi from myfunc
 755 MainThread Hello from main
1007 Thread-1 Hi from myfunc
1507 MainThread Hello from main
1508 Thread-1 Hi from myfunc
2010 Thread-1 Hi from myfunc
2258 MainThread Hello from main
2512 Thread-1 Hi from myfunc
3009 MainThread Hello from main
3013 Thread-1 Hi from myfunc
3515 Thread-1 Hi from myfunc
3761 MainThread Hello from main
4017 Thread-1 Hi from myfunc
4513 MainThread Hello from main
4518 Thread-1 Hi from myfunc
```

这表明日志记录输出散布在一个人们可能期望的位置。当然，这种方法适用于比此处所示更多的线程。

### 多个处理程序和格式化程序

记录器是普通的Python对象。该[`addHandler()`](https://docs.python.org/3/library/logging.html#logging.Logger.addHandler "logging.Logger.addHandler")方法没有您可以添加的处理程序数量的最小或最大配额。有时，应用程序将所有严重性的所有消息记录到文本文件，同时将错误或更高版本记录到控制台是有益的。要进行此设置，只需配置适当的处理程序即可。应用程序代码中的日志记录调用将保持不变。以下是对先前基于模块的简单配置示例的略微修改：

```python
import logging

logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('spam.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')
```

请注意，“应用程序”代码不关心多个处理程序。所有改变的是添加和配置名为*fh*的新处理程序。

在编写和测试应用程序时，创建具有更高或更低严重性过滤器的新处理程序的能力非常有用。`print`使用`logger.debug`：与您必须删除或稍后注释掉的print语句不同，logger.debug语句可以在源代码中保持不变，并且在您再次需要它们之前保持休眠状态，而不是使用许多语句进行调试。那时，唯一需要改变的是修改记录器和/或处理程序的严重性级别以进行调试。

### 记录到多个目的地

假设您要在不同的情况下使用不同的消息格式登录到控制台和文件。假设您要将具有DEBUG及更高级别的消息记录到文件，并将那些级别为INFO及更高级别的消息记录到控制台。我们还假设该文件应包含时间戳，但控制台消息不应该包含时间戳。以下是如何实现这一目标：

```python
import logging

# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s  %(name)-12s  %(levelname)-8s  %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='tmp.log',
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s  %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

# Now, we can log to the root logger, or any other logger. First the root...
logging.info('Jackdaws love my big sphinx of quartz.')

# Now, define a couple of other loggers which might represent areas in your
# application:

logger1 = logging.getLogger('myapp.area1')
logger2 = logging.getLogger('myapp.area2')

logger1.debug('Quick zephyrs blow, vexing daft Jim.')
logger1.info('How quickly daft jumping zebras vex.')
logger2.warning('Jail zesty vixen who grabbed pay from quack.')
logger2.error('The five boxing wizards jump quickly.')
```

当你运行它时，你会在控制台上看到

```
root        : INFO     Jackdaws love my big sphinx of quartz.
myapp.area1 : INFO     How quickly daft jumping zebras vex.
myapp.area2 : WARNING  Jail zesty vixen who grabbed pay from quack.
myapp.area2 : ERROR    The five boxing wizards jump quickly.
```

在tmp.log文件中你会看到类似的东西

```
10-22 22:19 root         INFO     Jackdaws love my big sphinx of quartz.
10-22 22:19 myapp.area1  DEBUG    Quick zephyrs blow, vexing daft Jim.
10-22 22:19 myapp.area1  INFO     How quickly daft jumping zebras vex.
10-22 22:19 myapp.area2  WARNING  Jail zesty vixen who grabbed pay from quack.
10-22 22:19 myapp.area2  ERROR    The five boxing wizards jump quickly.
```

如您所见，DEBUG消息仅显示在文件中。其他消息将发送到两个目的地。

此示例使用控制台和文件处理程序，但您可以使用您选择的任何数量和组合的处理程序。

### 配置服务器示例

以下是使用日志记录配置服务器的模块示例：

```python
import logging
import logging.config
import time
import os

# read initial config file
logging.config.fileConfig('logging.conf')

# create and start listener on port 9999
t = logging.config.listen(9999)
t.start()

logger = logging.getLogger('simpleExample')

try:
    # loop through logging calls to see the difference
    # new configurations make, until Ctrl+C is pressed
    while True:
        logger.debug('debug message')
        logger.info('info message')
        logger.warn('warn message')
        logger.error('error message')
        logger.critical('critical message')
        time.sleep(5)
except KeyboardInterrupt:
    # cleanup
    logging.config.stopListening()
    t.join()
```

这是一个脚本，它采用文件名并将该文件发送到服务器，正确地以二进制编码长度开头，作为新的日志记录配置：

```python
#!/usr/bin/env python
import socket, sys, struct

with open(sys.argv[1], 'rb') as f:
    data_to_send = f.read()

HOST = 'localhost'
PORT = 9999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('connecting...')
s.connect((HOST, PORT))
print('sending config...')
s.send(struct.pack('>L', len(data_to_send)))
s.send(data_to_send)
s.close()
print('complete')
```

### 处理阻止的处理程序

有时您必须让您的日志记录处理程序在不阻止您记录的线程的情况下完成工作。这在Web应用程序中很常见，当然它也会在其他场景中出现。

表现出缓慢行为的常见罪魁祸首是 [`SMTPHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.SMTPHandler "logging.handlers.SMTPHandler")：由于开发人员无法控制的多种原因(例如，性能不佳的邮件或网络基础设施)，发送电子邮件可能需要很长时间。但是几乎所有基于网络的处理程序都可以阻止：甚至一个[`SocketHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.SocketHandler "logging.handlers.SocketHandler")操作也可能在底层进行DNS查询，这太慢了(这个查询可以深入socket库代码，在Python层之下，在你的控件之外)。

有两种解决方案。第一种仅将 [`QueueHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.QueueHandler "logging.handlers.QueueHandler")附加到从性能关键线程访问的那些记录器。他们只是写入他们的队列，队列可以调整到足够大的容量或初始化，没有上限到他们的大小。通常会快速接受对队列的写入，但您可能需要捕获[`queue.Full`](https://docs.python.org/3/library/queue.html#queue.Full "queue.Full")异常作为代码中的预防措施。如果您是在其代码中具有性能关键线程的库开发人员，请务必记录此文档(以及仅附加`QueueHandlers`到记录器的建议)，以便其他将使用您的代码的开发人员受益。

解决方案的第二种方法[`QueueListener`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.QueueListener "logging.handlers.QueueListener")是设计为对应的[`QueueHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.QueueHandler "logging.handlers.QueueHandler")。A [`QueueListener`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.QueueListener "logging.handlers.QueueListener")非常简单：它传递了一个队列和一些处理程序，它会激活一个内部线程，该线程监听其队列中发送的LogRecords `QueueHandlers`(或其他任何来源`LogRecords`)。将`LogRecords`被从队列中删除，并传递到处理程序进行处理。

拥有一个单独的[`QueueListener`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.QueueListener "logging.handlers.QueueListener")类的优点是您可以使用相同的实例来为多个服务提供服务`QueueHandlers`。这比使用现有处理程序类的线程版本更加资源友好，每个处理程序会占用一个线程而没有特别的好处。

下面是使用这两个类的示例(省略了导入)：

```python
que = queue.Queue(-1)  # no limit on size
queue_handler = QueueHandler(que)
handler = logging.StreamHandler()
listener = QueueListener(que, handler)
root = logging.getLogger()
root.addHandler(queue_handler)
formatter = logging.Formatter('%(threadName)s: %(message)s')
handler.setFormatter(formatter)
listener.start()
# The log output will display the thread which generated
# the event (the main thread) rather than the internal
# thread which monitors the internal queue. This is what
# you want to happen.
root.warning('Look out!')
listener.stop()
```

在运行时，它将产生：

```
MainThread: Look out!
```

在3.5版中更改：在Python 3.5之前，[`QueueListener`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.QueueListener "logging.handlers.QueueListener")始终将从队列接收的每条消息传递给它初始化的每个处理程序。(这是因为假设级别过滤全部都在队列填充的另一侧完成。)从3.5开始，可以通过将关键字参数传递`respect_handler_level=True`给侦听器的构造函数来更改此行为。完成此操作后，侦听器会将每个消息的级别与处理程序的级别进行比较，并且只有在适当的情况下才会将消息传递给处理程序。

### 通过网络发送和接收日志记录事件

假设您希望通过网络发送日志记录事件，并在接收端处理它们。执行此操作的一种简单方法是将[`SocketHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.SocketHandler "logging.handlers.SocketHandler")实例附加 到发送端的根记录器：

```python
import logging, logging.handlers

rootLogger = logging.getLogger('')
rootLogger.setLevel(logging.DEBUG)
socketHandler = logging.handlers.SocketHandler('localhost',
                    logging.handlers.DEFAULT_TCP_LOGGING_PORT)
# don't bother with a formatter, since a socket handler sends the event as
# an unformatted pickle
rootLogger.addHandler(socketHandler)

# Now, we can log to the root logger, or any other logger. First the root...
logging.info('Jackdaws love my big sphinx of quartz.')

# Now, define a couple of other loggers which might represent areas in your
# application:

logger1 = logging.getLogger('myapp.area1')
logger2 = logging.getLogger('myapp.area2')

logger1.debug('Quick zephyrs blow, vexing daft Jim.')
logger1.info('How quickly daft jumping zebras vex.')
logger2.warning('Jail zesty vixen who grabbed pay from quack.')
logger2.error('The five boxing wizards jump quickly.')
```

在接收端，您可以使用该[`socketserver`](https://docs.python.org/3/library/socketserver.html#module-socketserver "socketserver：网络服务器的框架。") 模块设置接收器。这是一个基本的工作示例：

```python import pickle
import logging
import logging.handlers
import socketserver
import struct

class LogRecordStreamHandler(socketserver.StreamRequestHandler):
    """Handler for a streaming logging request.

 This basically logs the record using whatever logging policy is
 configured locally.
 """

    def handle(self):
        """
 Handle multiple requests - each expected to be a 4-byte length,
 followed by the LogRecord in pickle format. Logs the record
 according to whatever policy is configured locally.
 """
        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack('>L', chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.connection.recv(slen - len(chunk))
            obj = self.unPickle(chunk)
            record = logging.makeLogRecord(obj)
            self.handleLogRecord(record)

    def unPickle(self, data):
        return pickle.loads(data)

    def handleLogRecord(self, record):
        # if a name is specified, we use the named logger rather than the one
        # implied by the record.
        if self.server.logname is not None:
            name = self.server.logname
        else:
            name = record.name
        logger = logging.getLogger(name)
        # N.B. EVERY record gets logged. This is because Logger.handle
        # is normally called AFTER logger-level filtering. If you want
        # to do filtering, do it at the client end to save wasting
        # cycles and network bandwidth!
        logger.handle(record)

class LogRecordSocketReceiver(socketserver.ThreadingTCPServer):
    """
 Simple TCP socket-based logging receiver suitable for testing.
 """

    allow_reuse_address = True

    def __init__(self, host='localhost',
                 port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
                 handler=LogRecordStreamHandler):
        socketserver.ThreadingTCPServer.__init__(self, (host, port), handler)
        self.abort = 0
        self.timeout = 1
        self.logname = None

    def serve_until_stopped(self):
        import select
        abort = 0
        while not abort:
            rd, wr, ex = select.select([self.socket.fileno()],
                                       [], [],
                                       self.timeout)
            if rd:
                self.handle_request()
            abort = self.abort

def main():
    logging.basicConfig(
        format='%(relativeCreated)5d  %(name)-15s  %(levelname)-8s  %(message)s')
    tcpserver = LogRecordSocketReceiver()
    print('About to start TCP server...')
    tcpserver.serve_until_stopped()

if __name__ == '__main__':
    main()
```

首先运行服务器，然后运行客户端。在客户端，控制台上没有打印任何内容; 在服务器端，你应该看到类似的东西：

```
About to start TCP server...
   59 root            INFO     Jackdaws love my big sphinx of quartz.
   59 myapp.area1     DEBUG    Quick zephyrs blow, vexing daft Jim.
   69 myapp.area1     INFO     How quickly daft jumping zebras vex.
   69 myapp.area2     WARNING  Jail zesty vixen who grabbed pay from quack.
   69 myapp.area2     ERROR    The five boxing wizards jump quickly.
```

请注意，在某些情况下，pickle存在一些安全问题。如果这些影响到您，您可以通过覆盖`makePickle()`方法并在那里实现替代方法来使用替代序列化方案，以及调整上述脚本以使用替代序列化。

### 将上下文信息添加到日志输出中

有时，除了传递给日志记录调用的参数之外，您还希望日志记录输出包含上下文信息。例如，在联网应用程序中，可能需要在日志中记录客户端特定信息(例如，远程客户端的用户名或IP地址)。虽然您可以使用*额外的*参数来实现这一点，但以这种方式传递信息并不总是方便。尽管`Logger`在每个连接的基础上创建实例可能很诱人 ，但这不是一个好主意，因为这些实例不是垃圾回收。虽然这在实践中不是问题，但是当`Logger`实例的数量取决于您要在记录应用程序时使用的粒度级别时，如果实例的数量可能很难管理`Logger` 实例变得有效无限。

### 使用LoggerAdapters传递上下文信息

您可以通过简单的方式将上下文信息与记录事件信息一起输出，即使用`LoggerAdapter`该类。此类设计看起来像一个`Logger`，这样就可以调用 `debug()`，`info()`，`warning()`，`error()`， `exception()`，`critical()`和`log()`。这些方法与其对应的签名具有相同的签名`Logger`，因此您可以交替使用这两种类型的实例。

当您创建实例时`LoggerAdapter`，您将传递一个 `Logger`实例和一个类似于dict的对象，其中包含您的上下文信息。当您在实例上调用其中一个日志记录方法时 `LoggerAdapter`，它会将调用委托给`Logger`传递给其构造函数的基础实例 ，并安排在委派调用中传递上下文信息。这是以下代码的片段 `LoggerAdapter`：

```python
def debug(self, msg, *args, **kwargs):
    """
 Delegate a debug call to the underlying logger, after adding
 contextual information from this adapter instance.
 """
    msg, kwargs = self.process(msg, kwargs)
    self.logger.debug(msg, *args, **kwargs)
```

所述`process()`的方法`LoggerAdapter`是，其中所述上下文信息被添加到所述日志输出。它传递了日志记录调用的消息和关键字参数，并传回(可能)修改后的这些版本以用于对底层记录器的调用。此方法的默认实现仅保留消息，但在关键字参数中插入“额外”键，其值为传递给构造函数的类似dict的对象。当然，如果您在调用适配器时传递了一个'extra'关键字参数，它将被静默覆盖。

使用'extra'的优点是类似于dict的对象中的值被合并到`LogRecord`实例的__dict__中，允许您在实例中使用自定义字符串，这些`Formatter`实例知道类似dict的对象的键。如果您需要一个不同的方法，例如，如果您想要将上下文信息前置或附加到消息字符串，您只需要子类化`LoggerAdapter`和覆盖 `process()`以执行您需要的操作。这是一个简单的例子：

```python
class CustomAdapter(logging.LoggerAdapter):
    """
 This example adapter expects the passed in dict-like object to have a
 'connid' key, whose value in brackets is prepended to the log message.
 """
    def process(self, msg, kwargs):
        return '[%s] %s' % (self.extra['connid'], msg), kwargs
```

您可以这样使用：

```python
logger = logging.getLogger(__name__)
adapter = CustomAdapter(logger, {'connid': some_conn_id})
```

然后，您登录到适配器的任何事件都将具有`some_conn_id`预先添加到日志消息的值 。

#### 使用除dicts之外的对象来传递上下文信息

你并不需要一个实际的字典传递给一个`LoggerAdapter`-你可以通过它实现了一个类的实例`__getitem__`，并`__iter__`使它看起来像一个字典来记录。如果要动态生成值(而dict中的值将是常量)，这将非常有用。

#### 使用过滤器传递上下文信息

您还可以使用用户定义将上下文信息添加到日志输出 `Filter`。`Filter`允许实例修改`LogRecords` 传递给它们的实例，包括添加其他属性，然后可以使用合适的格式字符串输出，或者如果需要自定义`Formatter`。

例如，在Web应用程序中，正在处理的请求(或至少其中有趣的部分)可以存储在threadlocal([`threading.local`](https://docs.python.org/3/library/threading.html#threading.local "threading.local"))变量中，然后从a中访问`Filter`以添加来自请求的信息 - 例如，远程IP地址和远程用户的用户名 - `LogRecord`使用属性名称'ip'和'user'，如上`LoggerAdapter`例所示。在这种情况下，可以使用相同的格式字符串来获得与上面显示的类似的输出。这是一个示例脚本：

```python
import logging
from random import choice

class ContextFilter(logging.Filter):
    """
 This is a filter which injects contextual information into the log.

 Rather than use actual contextual information, we just use random
 data in this demo.
 """

    USERS = ['jim', 'fred', 'sheila']
    IPS = ['123.231.231.123', '127.0.0.1', '192.168.0.1']

    def filter(self, record):

        record.ip = choice(ContextFilter.IPS)
        record.user = choice(ContextFilter.USERS)
        return True

if __name__ == '__main__':
    levels = (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)-15s  %(name)-5s  %(levelname)-8s IP: %(ip)-15s User: %(user)-8s  %(message)s')
    a1 = logging.getLogger('a.b.c')
    a2 = logging.getLogger('d.e.f')

    f = ContextFilter()
    a1.addFilter(f)
    a2.addFilter(f)
    a1.debug('A debug message')
    a1.info('An info message with %s', 'some parameters')
    for x in range(10):
        lvl = choice(levels)
        lvlname = logging.getLevelName(lvl)
        a2.log(lvl, 'A message at %s level with %d  %s', lvlname, 2, 'parameters')
```

在运行时，产生类似于：

```
2010-09-06 22:38:15,292 a.b.c DEBUG    IP: 123.231.231.123 User: fred     A debug message
2010-09-06 22:38:15,300 a.b.c INFO     IP: 192.168.0.1     User: sheila   An info message with some parameters
2010-09-06 22:38:15,300 d.e.f CRITICAL IP: 127.0.0.1       User: sheila   A message at CRITICAL level with 2 parameters
2010-09-06 22:38:15,300 d.e.f ERROR    IP: 127.0.0.1       User: jim      A message at ERROR level with 2 parameters
2010-09-06 22:38:15,300 d.e.f DEBUG    IP: 127.0.0.1       User: sheila   A message at DEBUG level with 2 parameters
2010-09-06 22:38:15,300 d.e.f ERROR    IP: 123.231.231.123 User: fred     A message at ERROR level with 2 parameters
2010-09-06 22:38:15,300 d.e.f CRITICAL IP: 192.168.0.1     User: jim      A message at CRITICAL level with 2 parameters
2010-09-06 22:38:15,300 d.e.f CRITICAL IP: 127.0.0.1       User: sheila   A message at CRITICAL level with 2 parameters
2010-09-06 22:38:15,300 d.e.f DEBUG    IP: 192.168.0.1     User: jim      A message at DEBUG level with 2 parameters
2010-09-06 22:38:15,301 d.e.f ERROR    IP: 127.0.0.1       User: sheila   A message at ERROR level with 2 parameters
2010-09-06 22:38:15,301 d.e.f DEBUG    IP: 123.231.231.123 User: fred     A message at DEBUG level with 2 parameters
2010-09-06 22:38:15,301 d.e.f INFO     IP: 123.231.231.123 User: fred     A message at INFO level with 2 parameters
```

### 从多个进程记录到单个文件

虽然记录是线程安全的，并登录到从多个线程在单个进程中的单个文件*的*支持，记录从一个文件 *的多个进程*是*不*支持的，因为能够连续访问多个单个文件没有标准的方法Python中的进程。如果需要从多个进程登录到单个文件，则执行此操作的一种方法是让所有进程都记录到a `SocketHandler`，并且具有单独的进程，该进程实现从套接字读取并记录到文件的套接字服务器。(如果您愿意，可以在一个现有进程中专用一个线程来执行此功能。)[本节](https://docs.python.org/3/howto/logging-cookbook.html#network-logging) 更详细地记录了这种方法，并包括一个工作套接字接收器，可以作为您在自己的应用程序中适应的起点。

如果您使用的是包含该[`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing "多处理：基于进程的并行性。")模块的最新版本的Python ，您可以编写自己的处理程序，该处理程序使用[`Lock`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Lock "multiprocessing.Lock")此模块中的 类来序列化对您的进程中的文件的访问。现有的`FileHandler`和子类目前没有使用[`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing "多处理：基于进程的并行性。")，尽管它们将来可能会这样做。请注意，目前，该[`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing "多处理：基于进程的并行性。")模块并未在所有平台上提供工作锁功能(请参阅 [https://bugs.python.org/issue3770](https://bugs.python.org/issue3770))。

或者，您可以使用a `Queue`和a [`QueueHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.QueueHandler "logging.handlers.QueueHandler")将所有日志记录事件发送到多进程应用程序中的一个进程。以下示例脚本演示了如何执行此操作; 在示例中，单独的侦听器进程侦听其他进程发送的事件，并根据其自己的日志记录配置进行记录。虽然该示例仅演示了一种方法(例如，您可能希望使用侦听器线程而不是单独的侦听器进程 - 实现类似)但它确实允许侦听器和其他进程完全不同的日志记录配置在您的应用程序中，可以用作满足您自己特定要求的代码的基础：

```python
# You'll need these imports in your own code
import logging
import logging.handlers
import multiprocessing

# Next two import lines for this demo only
from random import choice, random
import time

#
# Because you'll want to define the logging configurations for listener and workers, the
# listener and worker process functions take a configurer parameter which is a callable
# for configuring logging for that process. These functions are also passed the queue,
# which they use for communication.
#
# In practice, you can configure the listener however you want, but note that in this
# simple example, the listener does not apply level or filter logic to received records.
# In practice, you would probably want to do this logic in the worker processes, to avoid
# sending events which would be filtered out between processes.
#
# The size of the rotated files is made small so you can see the results easily.
def listener_configurer():
    root = logging.getLogger()
    h = logging.handlers.RotatingFileHandler('mptest.log', 'a', 300, 10)
    f = logging.Formatter('%(asctime)s  %(processName)-10s  %(name)s  %(levelname)-8s  %(message)s')
    h.setFormatter(f)
    root.addHandler(h)

# This is the listener process top-level loop: wait for logging events
# (LogRecords)on the queue and handle them, quit when you get a None for a
# LogRecord.
def listener_process(queue, configurer):
    configurer()
    while True:
        try:
            record = queue.get()
            if record is None:  # We send this as a sentinel to tell the listener to quit.
                break
            logger = logging.getLogger(record.name)
            logger.handle(record)  # No level or filter logic applied - just do it!
        except Exception:
            import sys, traceback
            print('Whoops! Problem:', file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

# Arrays used for random selections in this demo

LEVELS = [logging.DEBUG, logging.INFO, logging.WARNING,
          logging.ERROR, logging.CRITICAL]

LOGGERS = ['a.b.c', 'd.e.f']

MESSAGES = [
    'Random message #1',
    'Random message #2',
    'Random message #3',
]

# The worker configuration is done at the start of the worker process run.
# Note that on Windows you can't rely on fork semantics, so each process
# will run the logging configuration code when it starts.
def worker_configurer(queue):
    h = logging.handlers.QueueHandler(queue)  # Just the one handler needed
    root = logging.getLogger()
    root.addHandler(h)
    # send all messages, for demo; no other level or filter logic applied.
    root.setLevel(logging.DEBUG)

# This is the worker process top-level loop, which just logs ten events with
# random intervening delays before terminating.
# The print messages are just so you know it's doing something!
def worker_process(queue, configurer):
    configurer(queue)
    name = multiprocessing.current_process().name
    print('Worker started: %s' % name)
    for i in range(10):
        time.sleep(random())
        logger = logging.getLogger(choice(LOGGERS))
        level = choice(LEVELS)
        message = choice(MESSAGES)
        logger.log(level, message)
    print('Worker finished: %s' % name)

# Here's where the demo gets orchestrated. Create the queue, create and start
# the listener, create ten workers and start them, wait for them to finish,
# then send a None to the queue to tell the listener to finish.
def main():
    queue = multiprocessing.Queue(-1)
    listener = multiprocessing.Process(target=listener_process,
                                       args=(queue, listener_configurer))
    listener.start()
    workers = []
    for i in range(10):
        worker = multiprocessing.Process(target=worker_process,
                                         args=(queue, worker_configurer))
        workers.append(worker)
        worker.start()
    for w in workers:
        w.join()
    queue.put_nowait(None)
    listener.join()

if __name__ == '__main__':
    main()
```

上述脚本的变体在单独的线程中保留主进程中的日志记录：

```python
import logging
import logging.config
import logging.handlers
from multiprocessing import Process, Queue
import random
import threading
import time

def logger_thread(q):
    while True:
        record = q.get()
        if record is None:
            break
        logger = logging.getLogger(record.name)
        logger.handle(record)

def worker_process(q):
    qh = logging.handlers.QueueHandler(q)
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(qh)
    levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR,
              logging.CRITICAL]
    loggers = ['foo', 'foo.bar', 'foo.bar.baz',
               'spam', 'spam.ham', 'spam.ham.eggs']
    for i in range(100):
        lvl = random.choice(levels)
        logger = logging.getLogger(random.choice(loggers))
        logger.log(lvl, 'Message no. %d', i)

if __name__ == '__main__':
    q = Queue()
    d = {
        'version': 1,
        'formatters': {
            'detailed': {
                'class': 'logging.Formatter',
                'format': '%(asctime)s  %(name)-15s  %(levelname)-8s  %(processName)-10s  %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
            },
            'file': {
                'class': 'logging.FileHandler',
                'filename': 'mplog.log',
                'mode': 'w',
                'formatter': 'detailed',
            },
            'foofile': {
                'class': 'logging.FileHandler',
                'filename': 'mplog-foo.log',
                'mode': 'w',
                'formatter': 'detailed',
            },
            'errors': {
                'class': 'logging.FileHandler',
                'filename': 'mplog-errors.log',
                'mode': 'w',
                'level': 'ERROR',
                'formatter': 'detailed',
            },
        },
        'loggers': {
            'foo': {
                'handlers': ['foofile']
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'file', 'errors']
        },
    }
    workers = []
    for i in range(5):
        wp = Process(target=worker_process, name='worker %d' % (i + 1), args=(q,))
        workers.append(wp)
        wp.start()
    logging.config.dictConfig(d)
    lp = threading.Thread(target=logger_thread, args=(q,))
    lp.start()
    # At this point, the main process could do some useful work of its own
    # Once it's done that, it can wait for the workers to terminate...
    for wp in workers:
        wp.join()
    # And now tell the logging thread to finish up, too
    q.put(None)
    lp.join()
```

此变体显示了如何为特定记录器应用配置 - 例如，`foo`记录器具有一个特殊的处理程序，它将`foo`子系统中的所有事件存储 在一个文件中`mplog-foo.log`。这将由主进程中的日志记录机制使用(即使在工作进程中生成日志记录事件)，以将消息定向到适当的目标。

### 使用文件旋转

有时您希望让日志文件增长到一定的大小，然后打开一个新文件并登录到该文件。您可能希望保留一定数量的这些文件，并且在创建了许多文件后，旋转文件以使文件数量和文件大小保持有限。对于此使用模式，日志包提供`RotatingFileHandler`：

```python
import glob
import logging
import logging.handlers

LOG_FILENAME = 'logging_rotatingfile_example.out'

# Set up a specific logger with our desired output level
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=20, backupCount=5)

my_logger.addHandler(handler)

# Log some messages
for i in range(20):
    my_logger.debug('i = %d' % i)

# See what files are created
logfiles = glob.glob('%s*' % LOG_FILENAME)

for filename in logfiles:
    print(filename)
```

结果应该是6个单独的文件，每个文件都包含应用程序的部分日志历史记录：

```python logging_rotatingfile_example.out
logging_rotatingfile_example.out.1
logging_rotatingfile_example.out.2
logging_rotatingfile_example.out.3
logging_rotatingfile_example.out.4
logging_rotatingfile_example.out.5
```

最新文件始终是`logging_rotatingfile_example.out`，每次达到大小限制时，都会使用后缀重命名 `.1`。重命名每个现有备份文件以增加后缀(`.1`变为`.2`等)并`.6`删除文件。

显然，这个例子将日志长度设置得太小，这是一个极端的例子。您可能希望将*maxBytes*设置为适当的值。

### 使用替代格式样式

将日志记录添加到Python标准库时，使用可变内容格式化消息的唯一方法是使用％-formatting方法。从那时起，Python已经获得了两种新的格式化方法:( [`string.Template`](https://docs.python.org/3/library/string.html#string.Template "string.Template")在Python 2.4中[`str.format()`](https://docs.python.org/3/library/stdtypes.html#str.format "str.format") 添加)和(在Python 2.6中添加)。

日志记录(截至3.2)为这两种额外的格式样式提供了改进的支持。该`Formatter`班已经增强，可以命名一个额外的，可选的关键字参数`style`。默认为 `'%'`，但其他可能的值是`'{'`和`'$'`，它们对应于其他两种格式样式。默认情况下会保持向后兼容性(正如您所期望的那样)，但通过显式指定样式参数，您可以指定使用[`str.format()`](https://docs.python.org/3/library/stdtypes.html#str.format "str.format")或的格式字符串 [`string.Template`](https://docs.python.org/3/library/string.html#string.Template "string.Template")。这是一个示例控制台会话，以显示可能性：

```python
>>> import logging
>>> root = logging.getLogger()
>>> root.setLevel(logging.DEBUG)
>>> handler = logging.StreamHandler()
>>> bf = logging.Formatter('{asctime} {name} {levelname:8s} {message}',
...                        style='{')
>>> handler.setFormatter(bf)
>>> root.addHandler(handler)
>>> logger = logging.getLogger('foo.bar')
>>> logger.debug('This is a DEBUG message')
2010-10-28 15:11:55,341 foo.bar DEBUG    This is a DEBUG message
>>> logger.critical('This is a CRITICAL message')
2010-10-28 15:12:11,526 foo.bar CRITICAL This is a CRITICAL message
>>> df = logging.Formatter('$asctime $name ${levelname} $message',
...                        style='/pre>)
>>> handler.setFormatter(df)
>>> logger.debug('This is a DEBUG message')
2010-10-28 15:13:06,924 foo.bar DEBUG This is a DEBUG message
>>> logger.critical('This is a CRITICAL message')
2010-10-28 15:13:11,494 foo.bar CRITICAL This is a CRITICAL message
>>>
```

请注意，最终输出到日志的日志记录消息的格式完全独立于单个日志消息的构造方式。那仍然可以使用％-formatting，如下所示：

```python
>>> logger.error('This is an%s  %s  %s', 'other,', 'ERROR,', 'message')
2010-10-28 15:19:29,833 foo.bar ERROR This is another, ERROR, message
>>>
```

记录调用(`logger.debug()`，`logger.info()`等)只取位置参数进行实际记录消息本身，只有用于确定如何处理该实际记录的电话选项中使用的关键字参数(例如，`exc_info`关键字参数以指示追溯信息应记录，或`extra`keyword参数，用于指示要添加到日志中的其他上下文信息)。因此，您无法使用[`str.format()`](https://docs.python.org/3/library/stdtypes.html#str.format "str.format")或[`string.Template`](https://docs.python.org/3/library/string.html#string.Template "string.Template")语法直接进行日志记录调用，因为日志记录包内部使用％-formatting来合并格式字符串和变量参数。在保留向后兼容性的同时不会改变这一点，因为现有代码中的所有日志记录调用都将使用％-format字符串。

但是，有一种方法可以使用{} - 和$ - 格式来构建单独的日志消息。回想一下，对于消息，您可以使用任意对象作为消息格式字符串，并且日志包将调用`str()`该对象以获取实际的格式字符串。考虑以下两个类：

```python
class BraceMessage:
    def __init__(self, fmt, *args, **kwargs):
        self.fmt = fmt
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return self.fmt.format(*self.args, **self.kwargs)

class DollarMessage:
    def __init__(self, fmt, **kwargs):
        self.fmt = fmt
        self.kwargs = kwargs

    def __str__(self):
        from string import Template
        return Template(self.fmt).substitute(**self.kwargs)
```

这些中的任何一个都可以用来代替格式字符串，以允许{} - 或$ -formatting用于构建实际的“消息”部分，该部分出现在格式化的日志输出中，而不是“％(message)s”或“{message}”或“$ message”。每当你想记录某些东西时使用类名都有点笨拙，但是如果你使用别名如__(双下划线 - 不要与_混淆，单个下划线用作同义词/别名[`gettext.gettext()`](https://docs.python.org/3/library/gettext.html#gettext.gettext "gettext.gettext")或者它的弟兄们)。

上述类不包含在Python中，尽管它们很容易复制并粘贴到您自己的代码中。它们可以如下使用(假设它们在一个名为的模块中声明`wherever`)：

```python
>>> from wherever import BraceMessage as __
>>> print(__('Message with {0} {name}', 2, name='placeholders'))
Message with 2 placeholders
>>> class Point: pass
...
>>> p = Point()
>>> p.x = 0.5
>>> p.y = 0.5
>>> print(__('Message with coordinates: ({point.x:.2f}, {point.y:.2f})',
...       point=p))
Message with coordinates: (0.50, 0.50)
>>> from wherever import DollarMessage as __
>>> print(__('Message with $num $what', num=2, what='placeholders'))
Message with 2 placeholders
>>>
```

虽然以上示例用于`print()`显示格式如何工作，但您当然会使用`logger.debug()`或类似于使用此方法实际记录。

需要注意的一点是，使用这种方法不会显着降低性能损失：实际格式化不是在您进行日志记录调用时发生的，而是在(和如果)记录消息实际上即将由处理程序输出到日志时。所以唯一可能引起你兴趣的有点不寻常的事情就是括号绕着格式字符串和参数，而不仅仅是格式字符串。这是因为__表示法只是对其中一个XXXMessage类的构造函数调用的语法糖。

如果您愿意，可以使用a `LoggerAdapter`来实现与上面类似的效果，如下例所示：

```python
import logging

class Message(object):
    def __init__(self, fmt, args):
        self.fmt = fmt
        self.args = args

    def __str__(self):
        return self.fmt.format(*self.args)

class StyleAdapter(logging.LoggerAdapter):
    def __init__(self, logger, extra=None):
        super(StyleAdapter, self).__init__(logger, extra or {})

    def log(self, level, msg, *args, **kwargs):
        if self.isEnabledFor(level):
            msg, kwargs = self.process(msg, kwargs)
            self.logger._log(level, Message(msg, args), (), **kwargs)

logger = StyleAdapter(logging.getLogger(__name__))

def main():
    logger.debug('Hello, {}', 'world!')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
```

上述脚本应在使用Python 3.2或更高版本运行时记录消息。`Hello, world!`

### 自定义`LogRecord`

每个日志记录事件都由一个[`LogRecord`](https://docs.python.org/3/library/logging.html#logging.LogRecord "logging.LogRecord")实例表示。当一个事件被记录而没有被记录器的级别过滤掉时，[`LogRecord`](https://docs.python.org/3/library/logging.html#logging.LogRecord "logging.LogRecord")会创建一个a ，填充有关该事件的信息，然后传递给该记录器的处理程序(及其祖先，直到并包括记录器，进一步传播层次结构)被禁用)。在Python 3.2之前，只有两个地方完成了这个创建：

* [`Logger.makeRecord()`](https://docs.python.org/3/library/logging.html#logging.Logger.makeRecord "logging.Logger.makeRecord")，这是在记录事件的正常过程中调用的。这[`LogRecord`](https://docs.python.org/3/library/logging.html#logging.LogRecord "logging.LogRecord")直接调用以创建实例。
* [`makeLogRecord()`](https://docs.python.org/3/library/logging.html#logging.makeLogRecord "logging.makeLogRecord")，使用包含要添加到LogRecord的属性的字典调用。这通常在已经通过网络接收到合适的字典时被调用(例如，通过a的pickle形式[`SocketHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.SocketHandler "logging.handlers.SocketHandler")，或者通过json形式的jSON形式[`HTTPHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.HTTPHandler "logging.handlers.HTTPHandler"))。

这通常意味着如果你需要做一些特殊的事情 [`LogRecord`](https://docs.python.org/3/library/logging.html#logging.LogRecord "logging.LogRecord")，你必须做以下其中一件事。

* 创建自己的[`Logger`](https://docs.python.org/3/library/logging.html#logging.Logger "logging.Logger")子类，覆盖 [`Logger.makeRecord()`](https://docs.python.org/3/library/logging.html#logging.Logger.makeRecord "logging.Logger.makeRecord")并[`setLoggerClass()`](https://docs.python.org/3/library/logging.html#logging.setLoggerClass "logging.setLoggerClass") 在实例化任何您关心的记录器之前使用它。
* 添加[`Filter`](https://docs.python.org/3/library/logging.html#logging.Filter "logging.Filter")到记录器或处理程序，它在[`filter()`](https://docs.python.org/3/library/logging.html#logging.Filter.filter "logging.Filter.filter")调用其方法时执行所需的特殊操作 。

在(例如)几个不同的图书馆想要做不同的事情的情况下，第一种方法会有点笨拙。每个人都会尝试设置自己的[`Logger`](https://docs.python.org/3/library/logging.html#logging.Logger "logging.Logger")子类，最后这个子类会赢。

对于许多情况，第二种方法工作得相当好，但是不允许你使用例如的专用子类[`LogRecord`](https://docs.python.org/3/library/logging.html#logging.LogRecord "logging.LogRecord")。库开发人员可以在他们的记录器上设置合适的过滤器，但他们必须记住每次他们引入新的记录器时都这样做(他们只需添加新的包或模块并做

```python
logger = logging.getLogger(__name__)
```

在模块级别)。可能需要考虑的事情太多了。开发人员还可以将过滤器添加到[`NullHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.NullHandler "logging.NullHandler")附加到其顶级记录器的过滤器，但如果应用程序开发人员将处理程序附加到较低级别的库记录器，则不会调用此过滤器 - 因此该处理程序的输出不会反映库的意图开发商。

在Python 3.2及更高版本中，[`LogRecord`](https://docs.python.org/3/library/logging.html#logging.LogRecord "logging.LogRecord")创建是通过您可以指定的工厂完成的。工厂只是一个调用，您可以用设置 [`setLogRecordFactory()`](https://docs.python.org/3/library/logging.html#logging.setLogRecordFactory "logging.setLogRecordFactory")，并与询问 [`getLogRecordFactory()`](https://docs.python.org/3/library/logging.html#logging.getLogRecordFactory "logging.getLogRecordFactory")。使用与[`LogRecord`](https://docs.python.org/3/library/logging.html#logging.LogRecord "logging.LogRecord")构造函数相同的签名调用工厂，工厂[`LogRecord`](https://docs.python.org/3/library/logging.html#logging.LogRecord "logging.LogRecord") 的默认设置也是如此。

此方法允许自定义工厂控制LogRecord创建的所有方面。例如，您可以使用与此类似的模式返回子类，或者只是在创建后向记录添加一些其他属性：

```python
old_factory = logging.getLogRecordFactory()

def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    record.custom_attribute = 0xdecafbad
    return record

logging.setLogRecordFactory(record_factory)
```

这种模式允许不同的库将工厂链接在一起，只要它们不会覆盖彼此的属性或无意中覆盖标准提供的属性，就不会有任何意外。但是，应该记住，链中的每个链接都会为所有日志记录操作增加运行时开销，并且只有在使用a [`Filter`](https://docs.python.org/3/library/logging.html#logging.Filter "logging.Filter")不能提供所需结果时才应使用该技术。

### 子类化QueueHandler - 一个ZeroMQ示例

您可以使用`QueueHandler`子类将消息发送到其他类型的队列，例如ZeroMQ“发布”套接字。在下面的示例中，套接字是单独创建的并传递给处理程序(作为其“队列”)：

```python
import zmq   # using pyzmq, the Python binding for ZeroMQ
import json  # for serializing records portably

ctx = zmq.Context()
sock = zmq.Socket(ctx, zmq.PUB)  # or zmq.PUSH, or other suitable value
sock.bind('tcp://*:5556')        # or wherever

class ZeroMQSocketHandler(QueueHandler):
    def enqueue(self, record):
        self.queue.send_json(record.__dict__)

handler = ZeroMQSocketHandler(sock)
```

当然还有其他组织方式，例如传递处理程序创建套接字所需的数据：

```python class ZeroMQSocketHandler(QueueHandler):
    def __init__(self, uri, socktype=zmq.PUB, ctx=None):
        self.ctx = ctx or zmq.Context()
        socket = zmq.Socket(self.ctx, socktype)
        socket.bind(uri)
        super().__init__(socket)

    def enqueue(self, record):
        self.queue.send_json(record.__dict__)

    def close(self):
        self.queue.close()
```

### 子类化QueueListener - 一个ZeroMQ示例

您还可以子类化`QueueListener`以从其他类型的队列中获取消息，例如ZeroMQ“subscribe”套接字。这是一个例子：

```python
class ZeroMQSocketListener(QueueListener):
    def __init__(self, uri, *handlers, **kwargs):
        self.ctx = kwargs.get('ctx') or zmq.Context()
        socket = zmq.Socket(self.ctx, zmq.SUB)
        socket.setsockopt_string(zmq.SUBSCRIBE, '')  # subscribe to everything
        socket.connect(uri)
        super().__init__(socket, *handlers, **kwargs)

    def dequeue(self):
        msg = self.queue.recv_json()
        return logging.makeLogRecord(msg)
```

### 基于字典的配置示例

下面是日志配置字典的示例 - 它来自[Django项目](https://docs.djangoproject.com/en/1.9/topics/logging/#configuring-logging)的[文档](https://docs.djangoproject.com/en/1.9/topics/logging/#configuring-logging)。传递此字典[`dictConfig()`](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig "logging.config.dictConfig")以使配置生效：

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s  %(asctime)s  %(module)s  %(process)d  %(thread)d  %(message)s'
        },
        'simple': {
            'format': '%(levelname)s  %(message)s'
        },
    },
    'filters': {
        'special': {
            '()': 'project.logging.SpecialFilter',
            'foo': 'bar',
        }
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['special']
        }
    },
    'loggers': {
        'django': {
            'handlers':['null'],
            'propagate': True,
            'level':'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'myproject.custom': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
            'filters': ['special']
        }
    }
}
```

有关此配置的更多信息，您可以查看 Django文档的[相关部分](https://docs.djangoproject.com/en/1.9/topics/logging/#configuring-logging)。

### 使用旋转器和命名器来自定义日志旋转处理

以下代码片段给出了如何定义名称和旋转器的示例，该片段显示了基于zlib的日志文件压缩：

```python
def namer(name):
    return name + ".gz"

def rotator(source, dest):
    with open(source, "rb") as sf:
        data = sf.read()
        compressed = zlib.compress(data, 9)
        with open(dest, "wb") as df:
            df.write(compressed)
    os.remove(source)

rh = logging.handlers.RotatingFileHandler(...)
rh.rotator = rotator
rh.namer = namer
```

这些不是*真正的*.gz文件，因为它们是裸压缩数据，没有“容器”，例如您在实际的gzip文件中找到的。此代码段仅用于说明目的。

### 更精细的多处理示例

以下工作示例显示了如何使用配置文件对多处理进行日志记录。配置相当简单，但用于说明如何在真正的多处理场景中实现更复杂的配置。

在该示例中，主进程生成一个侦听器进程和一些工作进程。每个主进程，监听器和工作者都有三个独立的配置(工作者都共享相同的配置)。我们可以看到主进程中的日志记录，工作者如何登录QueueHandler以及侦听器如何实现QueueListener以及更复杂的日志记录配置，并安排将通过队列接收的事件分派给配置中指定的处理程序。请注意，这些配置纯粹是说明性的，但您应该能够根据自己的方案调整此示例。

这是脚本 - 文档字符串和评论希望解释它是如何工作的：

```python
import logging
import logging.config
import logging.handlers
from multiprocessing import Process, Queue, Event, current_process
import os
import random
import time

class MyHandler:
    """
 A simple handler for logging events. It runs in the listener process and
 dispatches events to loggers based on the name in the received record,
 which then get dispatched, by the logging system, to the handlers
 configured for those loggers.
 """
    def handle(self, record):
        logger = logging.getLogger(record.name)
        # The process name is transformed just to show that it's the listener
        # doing the logging to files and console
        record.processName = '%s (for %s)' % (current_process().name, record.processName)
        logger.handle(record)

def listener_process(q, stop_event, config):
    """
 This could be done in the main process, but is just done in a separate
 process for illustrative purposes.

 This initialises logging according to the specified configuration,
 starts the listener and waits for the main process to signal completion
 via the event. The listener is then stopped, and the process exits.
 """
    logging.config.dictConfig(config)
    listener = logging.handlers.QueueListener(q, MyHandler())
    listener.start()
    if os.name == 'posix':
        # On POSIX, the setup logger will have been configured in the
        # parent process, but should have been disabled following the
        # dictConfig call.
        # On Windows, since fork isn't used, the setup logger won't
        # exist in the child, so it would be created and the message
        # would appear - hence the "if posix" clause.
        logger = logging.getLogger('setup')
        logger.critical('Should not appear, because of disabled logger ...')
    stop_event.wait()
    listener.stop()

def worker_process(config):
    """
 A number of these are spawned for the purpose of illustration. In
 practice, they could be a heterogeneous bunch of processes rather than
 ones which are identical to each other.

 This initialises logging according to the specified configuration,
 and logs a hundred messages with random levels to randomly selected
 loggers.

 A small sleep is added to allow other processes a chance to run. This
 is not strictly needed, but it mixes the output from the different
 processes a bit more than if it's left out.
 """
    logging.config.dictConfig(config)
    levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR,
              logging.CRITICAL]
    loggers = ['foo', 'foo.bar', 'foo.bar.baz',
               'spam', 'spam.ham', 'spam.ham.eggs']
    if os.name == 'posix':
        # On POSIX, the setup logger will have been configured in the
        # parent process, but should have been disabled following the
        # dictConfig call.
        # On Windows, since fork isn't used, the setup logger won't
        # exist in the child, so it would be created and the message
        # would appear - hence the "if posix" clause.
        logger = logging.getLogger('setup')
        logger.critical('Should not appear, because of disabled logger ...')
    for i in range(100):
        lvl = random.choice(levels)
        logger = logging.getLogger(random.choice(loggers))
        logger.log(lvl, 'Message no. %d', i)
        time.sleep(0.01)

def main():
    q = Queue()
    # The main process gets a simple configuration which prints to the console.
    config_initial = {
        'version': 1,
        'formatters': {
            'detailed': {
                'class': 'logging.Formatter',
                'format': '%(asctime)s  %(name)-15s  %(levelname)-8s  %(processName)-10s  %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
    }
    # The worker process configuration is just a QueueHandler attached to the
    # root logger, which allows all messages to be sent to the queue.
    # We disable existing loggers to disable the "setup" logger used in the
    # parent process. This is needed on POSIX because the logger will
    # be there in the child following a fork().
    config_worker = {
        'version': 1,
        'disable_existing_loggers': True,
        'handlers': {
            'queue': {
                'class': 'logging.handlers.QueueHandler',
                'queue': q,
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['queue']
        },
    }
    # The listener process configuration shows that the full flexibility of
    # logging configuration is available to dispatch events to handlers however
    # you want.
    # We disable existing loggers to disable the "setup" logger used in the
    # parent process. This is needed on POSIX because the logger will
    # be there in the child following a fork().
    config_listener = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'detailed': {
                'class': 'logging.Formatter',
                'format': '%(asctime)s  %(name)-15s  %(levelname)-8s  %(processName)-10s  %(message)s'
            },
            'simple': {
                'class': 'logging.Formatter',
                'format': '%(name)-15s  %(levelname)-8s  %(processName)-10s  %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'simple',
            },
            'file': {
                'class': 'logging.FileHandler',
                'filename': 'mplog.log',
                'mode': 'w',
                'formatter': 'detailed',
            },
            'foofile': {
                'class': 'logging.FileHandler',
                'filename': 'mplog-foo.log',
                'mode': 'w',
                'formatter': 'detailed',
            },
            'errors': {
                'class': 'logging.FileHandler',
                'filename': 'mplog-errors.log',
                'mode': 'w',
                'level': 'ERROR',
                'formatter': 'detailed',
            },
        },
        'loggers': {
            'foo': {
                'handlers': ['foofile']
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'file', 'errors']
        },
    }
    # Log some initial events, just to show that logging in the parent works
    # normally.
    logging.config.dictConfig(config_initial)
    logger = logging.getLogger('setup')
    logger.info('About to create workers ...')
    workers = []
    for i in range(5):
        wp = Process(target=worker_process, name='worker %d' % (i + 1),
                     args=(config_worker,))
        workers.append(wp)
        wp.start()
        logger.info('Started worker: %s', wp.name)
    logger.info('About to create listener ...')
    stop_event = Event()
    lp = Process(target=listener_process, name='listener',
                 args=(q, stop_event, config_listener))
    lp.start()
    logger.info('Started listener')
    # We now hang around for the workers to finish their work.
    for wp in workers:
        wp.join()
    # Workers all done, listening can now stop.
    # Logging in the parent still works normally.
    logger.info('Telling listener to stop ...')
    stop_event.set()
    lp.join()
    logger.info('All done.')

if __name__ == '__main__':
    main()
```

### 将BOM插入发送到SysLogHandler的消息中

[**RFC 5424**](https://tools.ietf.org/html/rfc5424.html)要求将Unicode消息作为一组字节发送到syslog守护程序，该字节具有以下结构：可选的纯ASCII组件，后跟UTF-8字节顺序标记(BOM)，然后使用UTF编码Unicode -8。(见 [**规范的相关部分**](https://tools.ietf.org/html/rfc5424.html#section-6)。)

在Python 3.1中，添加了代码 [`SysLogHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.SysLogHandler "logging.handlers.SysLogHandler")以将BOM插入到消息中，但不幸的是，它实现不正确，BOM出现在消息的开头，因此不允许任何纯ASCII组件出现在它之前。

由于此行为被破坏，正在从Python 3.2.4及更高版本中删除不正确的BOM插入代码。但是，它没有被替换，如果你想生产[](https://tools.ietf.org/html/rfc5424.html)符合[** RFC 5424**](https://tools.ietf.org/html/rfc5424.html)的消息包括BOM，可选的纯ASCII序列和之后的任意Unicode，使用UTF-8编码，然后您需要执行以下操作：

1. 使用以下格式字符串将[`Formatter`](https://docs.python.org/3/library/logging.html#logging.Formatter "logging.Formatter")实例附加到您的 [`SysLogHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.SysLogHandler "logging.handlers.SysLogHandler")实例：

    ```python
    'ASCII section\ufeffUnicode section'
    ```

    当使用UTF-8编码时，Unicode代码点U + FEFF将被编码为UTF-8 BOM - 字节串`b'\xef\xbb\xbf'`。

2. 用您喜欢的任何占位符替换ASCII部分，但要确保替换后出现的数据始终为ASCII(这样，在UTF-8编码后它将保持不变)。

3. 用你喜欢的任何占位符替换Unicode部分; 如果替换后出现的数据包含ASCII范围之外的字符，那很好 - 它将使用UTF-8进行编码。

格式化的消息*将*使用UTF-8编码进行编码 `SysLogHandler`。如果您遵守上述规则，您应该能够制作 [**符合RFC 5424**](https://tools.ietf.org/html/rfc5424.html)的消息。如果不这样做，日志记录可能不会抱怨，但您的消息将不符合RFC 5424，并且您的syslog守护程序可能会抱怨。

### 实现结构化日志记录

虽然大多数日志消息是供人阅读，因此不容易机解析的，有可能是要以结构化的格式输出消息的情况下*是*能够通过程序被解析(而不需要复杂的正则表达式解析日志消息)。使用日志包可以直接实现。有许多方法可以实现这一点，但以下是一种使用JSON以机器可解析的方式序列化事件的简单方法：

```python
import json
import logging

class StructuredMessage(object):
    def __init__(self, message, **kwargs):
        self.message = message
        self.kwargs = kwargs

    def __str__(self):
        return '%s >>> %s' % (self.message, json.dumps(self.kwargs))

_ = StructuredMessage   # optional, to improve readability

logging.basicConfig(level=logging.INFO, format='%(message)s')
logging.info(_('message 1', foo='bar', bar='baz', num=123, fnum=123.456))
```

如果运行上面的脚本，它会打印：

```
message 1 >>> {"fnum": 123.456, "num": 123, "bar": "baz", "foo": "bar"}
```

请注意，根据所使用的Python版本，项​​目的顺序可能会有所不同。

如果您需要更专业的处理，可以使用自定义JSON编码器，如以下完整示例所示：

```python
from __future__ import unicode_literals

import json
import logging

# This next bit is to ensure the script runs unchanged on 2.x and 3.x
try:
    unicode
except NameError:
    unicode = str

class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, set):
            return tuple(o)
        elif isinstance(o, unicode):
            return o.encode('unicode_escape').decode('ascii')
        return super(Encoder, self).default(o)

class StructuredMessage(object):
    def __init__(self, message, **kwargs):
        self.message = message
        self.kwargs = kwargs

    def __str__(self):
        s = Encoder().encode(self.kwargs)
        return '%s >>> %s' % (self.message, s)

_ = StructuredMessage   # optional, to improve readability

def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    logging.info(_('message 1', set_value={1, 2, 3}, snowman='\u2603'))

if __name__ == '__main__':
    main()
```

运行上面的脚本时，它会打印：

```
message 1 >>> {"snowman": "\u2603", "set_value": [1, 2, 3]}
```

请注意，根据所使用的Python版本，项​​目的顺序可能会有所不同。

### 使用自定义处理程序

有时您希望以特定方式自定义日志记录处理程序，如果您使用[`dictConfig()`](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig "logging.config.dictConfig")，则可以在不进行子类化的情况下执行此操作。例如，请考虑您可能要设置日志文件的所有权。在POSIX上，这很容易使用[`shutil.chown()`](https://docs.python.org/3/library/shutil.html#shutil.chown "shutil.chown")，但stdlib中的文件处理程序不提供内置支持。您可以使用普通函数自定义处理程序创建，例如：

```python
def owned_file_handler(filename, mode='a', encoding=None, owner=None):
    if owner:
        if not os.path.exists(filename):
            open(filename, 'a').close()
        shutil.chown(filename, *owner)
    return logging.FileHandler(filename, mode, encoding)
```

然后，您可以在传递给的日志记录配置中指定[`dictConfig()`](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig "logging.config.dictConfig")通过调用此函数来创建日志记录处理程序：

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s  %(levelname)s  %(name)s  %(message)s'
        },
    },
    'handlers': {
        'file':{
            # The values below are popped from this dictionary and
            # used to create the handler, set the handler's level and
            # its formatter.
            '()': owned_file_handler,
            'level':'DEBUG',
            'formatter': 'default',
            # The values below are passed to the handler creator callable
            # as keyword arguments.
            'owner': ['pulse', 'pulse'],
            'filename': 'chowntest.log',
            'mode': 'w',
            'encoding': 'utf-8',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'DEBUG',
    },
}
```

在此示例中，我使用`pulse`用户和组设置所有权，仅用于说明目的。将它们组合成一个工作脚本，`chowntest.py`：

```python
import logging, logging.config, os, shutil

def owned_file_handler(filename, mode='a', encoding=None, owner=None):
    if owner:
        if not os.path.exists(filename):
            open(filename, 'a').close()
        shutil.chown(filename, *owner)
    return logging.FileHandler(filename, mode, encoding)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s  %(levelname)s  %(name)s  %(message)s'
        },
    },
    'handlers': {
        'file':{
            # The values below are popped from this dictionary and
            # used to create the handler, set the handler's level and
            # its formatter.
            '()': owned_file_handler,
            'level':'DEBUG',
            'formatter': 'default',
            # The values below are passed to the handler creator callable
            # as keyword arguments.
            'owner': ['pulse', 'pulse'],
            'filename': 'chowntest.log',
            'mode': 'w',
            'encoding': 'utf-8',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'DEBUG',
    },
}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('mylogger')
logger.debug('A debug message')
```

要运行它，您可能需要运行`root`：

```python
$ sudo python3.3 chowntest.py
$ cat chowntest.log
2013-11-05 09:34:51,128 DEBUG mylogger A debug message
$ ls -l chowntest.log
-rw-r--r-- 1 pulse pulse 55 2013-11-05 09:34 chowntest.log
```

请注意，此示例使用Python 3.3，因为它[`shutil.chown()`](https://docs.python.org/3/library/shutil.html#shutil.chown "shutil.chown") 出现在哪里。这种方法适用于任何支持的Python版本[`dictConfig()`](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig "logging.config.dictConfig")- 即Python 2.7,3.2或更高版本。对于3.3之前的版本，您需要使用例如实现实际的所有权更改[`os.chown()`](https://docs.python.org/3/library/os.html#os.chown "os.chown")。

实际上，处理程序创建函数可能位于项目中某处的实用程序模块中。而不是配置中的行：

```python
'()': owned_file_handler,
```

你可以使用例如：

```python
'()': 'ext://project.util.owned_file_handler',
```

其中`project.util`可以替换为函数所在的包的实际名称。在上面的工作脚本中，使用`'ext://__main__.owned_file_handler'`应该工作。这里，实际的可调用[`dictConfig()`](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig "logging.config.dictConfig")来自`ext://`规范。

这个例子有希望指出如何实现其他类型的文件更改 - 例如设置特定的POSIX权限位 - 以相同的方式使用[`os.chmod()`](https://docs.python.org/3/library/os.html#os.chmod "os.chmod")。

当然，该方法也可以扩展到除了 [`FileHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.FileHandler "logging.FileHandler")- 例如，一个旋转文件处理程序，或者一个不同类型的处理程序之外的处理程序类型。

### 在整个应用程序中使用特定格式样式

在Python 3.2中，[`Formatter`](https://docs.python.org/3/library/logging.html#logging.Formatter "logging.Formatter")获得了一个`style`关键字参数，该参数虽然默认`%`为向后兼容，但允许指定`{`或`$`支持由[`str.format()`](https://docs.python.org/3/library/stdtypes.html#str.format "str.format")和支持的格式化方法[`string.Template`](https://docs.python.org/3/library/string.html#string.Template "string.Template")。请注意，这将控制最终输出到日志的日志消息的格式，并且与单个日志消息的构造方式完全正交。

记录调用([`debug()`](https://docs.python.org/3/library/logging.html#logging.Logger.debug "logging.Logger.debug")，[`info()`](https://docs.python.org/3/library/logging.html#logging.Logger.info "logging.Logger.info")等)只取位置参数进行实际记录消息本身，只有用于确定如何处理该调用的日志记录选项一起使用关键字参数(例如，`exc_info`关键字参数以指示追溯信息应记录，或`extra`关键字参数，用于指示要添加到日志中的其他上下文信息)。因此，您无法使用[`str.format()`](https://docs.python.org/3/library/stdtypes.html#str.format "str.format")或[`string.Template`](https://docs.python.org/3/library/string.html#string.Template "string.Template")语法直接进行日志记录调用，因为日志记录包内部使用％-formatting来合并格式字符串和变量参数。在保留向后兼容性的同时不会改变这一点，因为现有代码中的所有日志记录调用都将使用％-format字符串。

已有建议将格式样式与特定记录器相关联，但该方法也会遇到向后兼容性问题，因为任何现有代码都可能使用给定的记录器名称并使用％-formatting。

为了在任何第三方库和代码之间以互操作方式进行日志记录，需要在单个日志记录调用的级别上做出有关格式化的决策。这开辟了几种可以容纳替代格式样式的方法。

#### 使用LogRecord工厂

在Python 3.2中，除了[`Formatter`](https://docs.python.org/3/library/logging.html#logging.Formatter "logging.Formatter")上面提到的更改之外，日志包还能够允许用户[`LogRecord`](https://docs.python.org/3/library/logging.html#logging.LogRecord "logging.LogRecord")使用该[`setLogRecordFactory()`](https://docs.python.org/3/library/logging.html#logging.setLogRecordFactory "logging.setLogRecordFactory")函数设置自己的 子类。您可以使用它来设置自己的子类[`LogRecord`](https://docs.python.org/3/library/logging.html#logging.LogRecord "logging.LogRecord")，通过重写[`getMessage()`](https://docs.python.org/3/library/logging.html#logging.LogRecord.getMessage "logging.LogRecord.getMessage")方法来执行正确的操作。此方法的基类实现是格式化的位置，您可以在其中替换备用格式; 但是，您应该小心支持所有格式样式并允许％-formatting作为默认值，以确保与其他代码的互操作性。还应该注意`msg % args`，就像基础`str(self.msg)`实施一样。

请参阅有关的参考文档[`setLogRecordFactory()`](https://docs.python.org/3/library/logging.html#logging.setLogRecordFactory "logging.setLogRecordFactory")，并 [`LogRecord`](https://docs.python.org/3/library/logging.html#logging.LogRecord "logging.LogRecord")获取更多信息。

#### 使用自定义消息对象

还有另一种可能更简单的方法，您可以使用{} - 和$ - 格式来构建您的个人日志消息。您可能会记得(从 [使用任意对象作为消息](https://docs.python.org/3/howto/logging.html#arbitrary-object-messages))，在日志记录时，您可以使用任意对象作为消息格式字符串，并且日志记录包将调用 [`str()`](https://docs.python.org/3/library/stdtypes.html#str "海峡")该对象以获取实际的格式字符串。考虑以下两个类：

```python
class BraceMessage(object):
    def __init__(self, fmt, *args, **kwargs):
        self.fmt = fmt
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return self.fmt.format(*self.args, **self.kwargs)

class DollarMessage(object):
    def __init__(self, fmt, **kwargs):
        self.fmt = fmt
        self.kwargs = kwargs

    def __str__(self):
        from string import Template
        return Template(self.fmt).substitute(**self.kwargs)
```

这些中的任何一个都可以用来代替格式字符串，以允许{} - 或$ -formatting用于构建实际的“消息”部分，该部分出现在格式化的日志输出中，而不是“％(message)s”或“{message}”或“$ message”。如果你发现在你想要记录某些内容时使用类名有点笨拙，那么如果你使用别名(例如`M`或 `_`用于消息)(或者`__`，如果你`_`用于本地化)，你可以使它变得更加可口。

下面给出了这种方法的例子。首先，格式化`str.format()`：

```python
>>> __ = BraceMessage
>>> print(__('Message with {0}  {1}', 2, 'placeholders'))
Message with 2 placeholders
>>> class Point: pass
...
>>> p = Point()
>>> p.x = 0.5
>>> p.y = 0.5
>>> print(__('Message with coordinates: ({point.x:.2f}, {point.y:.2f})', point=p))
Message with coordinates: (0.50, 0.50)
```

其次，格式化`string.Template`：

```python
>>> __ = DollarMessage
>>> print(__('Message with $num $what', num=2, what='placeholders'))
Message with 2 placeholders
>>>
```

需要注意的一点是，使用这种方法不会显着降低性能损失：实际格式化不是在您进行日志记录调用时发生的，而是在(和如果)记录消息实际上即将由处理程序输出到日志时。所以唯一可能引起你兴趣的有点不寻常的事情就是括号绕着格式字符串和参数，而不仅仅是格式字符串。那是因为__表示法只是对`XXXMessage`上面显示的类之一的构造函数调用的语法糖。

### 使用配置过滤器`dictConfig()`

您*可以*使用配置过滤器[`dictConfig()`](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig "logging.config.dictConfig")，但乍看之下可能并不明显(如此配方)。由于 [`Filter`](https://docs.python.org/3/library/logging.html#logging.Filter "logging.Filter")是标准库中包含的唯一过滤器类，并且它不太可能满足许多​​要求(它仅作为基类)，因此通常需要[`Filter`](https://docs.python.org/3/library/logging.html#logging.Filter "logging.Filter") 使用重写[`filter()`](https://docs.python.org/3/library/logging.html#logging.Filter.filter "logging.Filter.filter")方法定义自己的子类。为此，请`()`在过滤器的配置字典中指定密钥，指定将用于创建过滤器的可调用对象(类是最明显的，但您可以提供任何返回[`Filter`](https://docs.python.org/3/library/logging.html#logging.Filter "logging.Filter")实例的可调用对象 )。这是一个完整的例子：

```python
import logging
import logging.config
import sys

class MyFilter(logging.Filter):
    def __init__(self, param=None):
        self.param = param

    def filter(self, record):
        if self.param is None:
            allow = True
        else:
            allow = self.param not in record.msg
        if allow:
            record.msg = 'changed: ' + record.msg
        return allow

LOGGING = {
    'version': 1,
    'filters': {
        'myfilter': {
            '()': MyFilter,
            'param': 'noshow',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['myfilter']
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console']
    },
}

if __name__ == '__main__':
    logging.config.dictConfig(LOGGING)
    logging.debug('hello')
    logging.debug('hello - noshow')
```

此示例显示如何以关键字参数的形式将配置数据传递给构造实例的callable。运行时，上面的脚本将打印：

```
changed: hello
```

这表明过滤器按配置工作。

需要注意几点：

* 如果您不能直接在配置中引用callable(例如，如果它位于不同的模块中，并且您无法直接将其导入配置字典的位置)，则可以使用[Access对外部对象中](https://docs.python.org/3/library/logging.config.html#logging-config-dict-externalobj)`ext://...`所述的表单。例如，您可以使用文本而不是上面的示例。[](https://docs.python.org/3/library/logging.config.html#logging-config-dict-externalobj)`'ext://__main__.MyFilter'``MyFilter`
* 除了过滤器，此技术还可用于配置自定义处理程序和格式化程序。有关日志记录如何在其配置中使用用户定义的对象支持的更多信息，请参阅[用户定义的对象](https://docs.python.org/3/library/logging.config.html#logging-config-dict-userdef)，并参阅上面的[dictConfig()使用dictConfig()定制处理程序](https://docs.python.org/3/howto/logging-cookbook.html#custom-handlers)。

### 自定义异常格式化

有时您可能希望进行自定义异常格式化 - 出于参数的考虑，假设您希望每个记录事件只有一行，即使存在异常信息也是如此。您可以使用自定义格式化程序类执行此操作，如以下示例所示：

```python
import logging

class OneLineExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        """
        Format an exception so that it prints on a single line.
        """
        result = super(OneLineExceptionFormatter, self).formatException(exc_info)
        return repr(result)  # or format into one line however you want to

    def format(self, record):
        s = super(OneLineExceptionFormatter, self).format(record)
        if record.exc_text:
            s = s.replace('\n', '') + '|'
        return s

def configure_logging():
    fh = logging.FileHandler('output.txt', 'w')
    f = OneLineExceptionFormatter('%(asctime)s|%(levelname)s|%(message)s|',
                                  '%d/%m/%Y %H:%M:%S')
    fh.setFormatter(f)
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(fh)

def main():
    configure_logging()
    logging.info('Sample message')
    try:
        x = 1 / 0
    except ZeroDivisionError as e:
        logging.exception('ZeroDivisionError: %s', e)

if __name__ == '__main__':
    main()
```

运行时，会生成一个恰好有两行的文件：

```python
28/01/2015 07:21:23|INFO|Sample message|
28/01/2015 07:21:23|ERROR|ZeroDivisionError: integer division or modulo by zero|'Traceback (most recent call last):\n  File "logtest7.py", line 30, in main\n    x = 1 / 0\nZeroDivisionError: integer division or modulo by zero'|
```

虽然上述处理过于简单，但它指出了如何根据自己的喜好格式化异常信息的方法。该[`traceback`](https://docs.python.org/3/library/traceback.html#module-traceback "traceback：打印或检索堆栈回溯。")模块可能有助于满足更多特殊需求。

### 说出日志消息

在某些情况下，需要以可听见的格式而不是可见的格式呈现日志消息。如果您的系统中有文本到语音(TTS)功能，即使它没有Python绑定，这也很容易实现。大多数TTS系统都有一个可以运行的命令行程序，这可以使用处理程序调用[`subprocess`](https://docs.python.org/3/library/subprocess.html#module-subprocess "subprocess：子进程管理。")。这里假设TTS命令行程序不希望与用户交互或需要很长时间才能完成，并且记录消息的频率不会高到使消息淹没用户，并且可以接受一次一个而不是同时发出的消息，下面的示例实现等待在处理下一个消息之前说出一条消息，这可能导致其他处理程序保持等待。这是一个简短的示例，显示了该方法，它假定`espeak`TTS包可用：

```python
import logging
import subprocess
import sys

class TTSHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        # Speak slowly in a female English voice
        cmd = ['espeak', '-s150', '-ven+f3', msg]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        # wait for the program to finish
        p.communicate()

def configure_logging():
    h = TTSHandler()
    root = logging.getLogger()
    root.addHandler(h)
    # the default formatter just returns the message
    root.setLevel(logging.DEBUG)

def main():
    logging.info('Hello')
    logging.debug('Goodbye')

if __name__ == '__main__':
    configure_logging()
    sys.exit(main())
```

运行时，这个脚本应该用女性的声音说出“Hello”然后再说“Goodbye”。

当然，上述方法可以适用于其他TTS系统甚至其他系统，它们可以通过从命令行运行的外部程序处理消息。

### 缓冲日志消息并有条件地输出它们

在某些情况下，您可能希望在临时区域中记录消息，并且只在发生某种情况时才输出消息。例如，您可能希望开始在函数中记录调试事件，并且如果函数完成且没有错误，您不希望使用收集的调试信息来混乱日志，但是如果出现错误，则需要所有调试要输出的信息以及错误。

下面是一个示例，说明如何使用装饰器为您的函数执行此操作，您希望日志记录以这种方式运行。它利用了[`logging.handlers.MemoryHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.MemoryHandler "logging.handlers.MemoryHandler")，它允许缓冲已记录的事件直到某些条件发生，此时缓冲的事件被`flushed` 传递给另一个处理程序(`target`处理程序)进行处理。默认情况下，`MemoryHandler`当缓冲区被填满时刷新或者看到级别大于或等于指定阈值的事件。`MemoryHandler`如果您想要自定义刷新行为，可以将此配方与更专业的子类一起使用。

示例脚本有一个简单的函数，它只`foo`循环遍历所有日志记录级别，写入以说明`sys.stderr`要登录的级别，然后实际记录该级别的消息。您可以传递一个参数`foo`，如果为true，将记录在ERROR和CRITICAL级别 - 否则，它只记录DEBUG，INFO和WARNING级别。

该脚本只是安排装饰`foo`一个装饰器，它将执行所需的条件记录。装饰器将记录器作为参数，并在对装饰函数的调用期间附加内存处理程序。可以使用目标处理程序，应该发生刷新的级别以及缓冲区的容量来额外地对装饰器进行参数化。这些默认到[`StreamHandler`](https://docs.python.org/3/library/logging.handlers.html#logging.StreamHandler "logging.StreamHandler")其写入`sys.stderr`， `logging.ERROR`并`100`分别。

这是脚本：

```python
import logging
from logging.handlers import MemoryHandler
import sys

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def log_if_errors(logger, target_handler=None, flush_level=None, capacity=None):
    if target_handler is None:
        target_handler = logging.StreamHandler()
    if flush_level is None:
        flush_level = logging.ERROR
    if capacity is None:
        capacity = 100
    handler = MemoryHandler(capacity, flushLevel=flush_level, target=target_handler)

    def decorator(fn):
        def wrapper(*args, **kwargs):
            logger.addHandler(handler)
            try:
                return fn(*args, **kwargs)
            except Exception:
                logger.exception('call failed')
                raise
            finally:
                super(MemoryHandler, handler).flush()
                logger.removeHandler(handler)
        return wrapper

    return decorator

def write_line(s):
    sys.stderr.write('%s\n' % s)

def foo(fail=False):
    write_line('about to log at DEBUG ...')
    logger.debug('Actually logged at DEBUG')
    write_line('about to log at INFO ...')
    logger.info('Actually logged at INFO')
    write_line('about to log at WARNING ...')
    logger.warning('Actually logged at WARNING')
    if fail:
        write_line('about to log at ERROR ...')
        logger.error('Actually logged at ERROR')
        write_line('about to log at CRITICAL ...')
        logger.critical('Actually logged at CRITICAL')
    return fail

decorated_foo = log_if_errors(logger)(foo)

if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    write_line('Calling undecorated foo with False')
    assert not foo(False)
    write_line('Calling undecorated foo with True')
    assert foo(True)
    write_line('Calling decorated foo with False')
    assert not decorated_foo(False)
    write_line('Calling decorated foo with True')
    assert decorated_foo(True)
```

运行此脚本时，应遵循以下输出：

```
Calling undecorated foo with False
about to log at DEBUG ...
about to log at INFO ...
about to log at WARNING ...
Calling undecorated foo with True
about to log at DEBUG ...
about to log at INFO ...
about to log at WARNING ...
about to log at ERROR ...
about to log at CRITICAL ...
Calling decorated foo with False
about to log at DEBUG ...
about to log at INFO ...
about to log at WARNING ...
Calling decorated foo with True
about to log at DEBUG ...
about to log at INFO ...
about to log at WARNING ...
about to log at ERROR ...
Actually logged at DEBUG
Actually logged at INFO
Actually logged at WARNING
Actually logged at ERROR
about to log at CRITICAL ...
Actually logged at CRITICAL
```

如您所见，实际日志记录输出仅在记录严重性为ERROR或更高的事件时发生，但在这种情况下，还会记录较低严重性的任何先前事件。

你当然可以使用传统的装饰方法：

```python
@log_if_errors(logger)
def foo(fail=False):
    ...
```

### 通过配置使用UTC(GMT)格式化时间

有时您希望使用UTC格式化时间，这可以使用`UTCFormatter`等类来完成，如下所示：

```python import logging
import time

class UTCFormatter(logging.Formatter):
    converter = time.gmtime
```

然后你可以`UTCFormatter`在你的代码中使用而不是 [`Formatter`](https://docs.python.org/3/library/logging.html#logging.Formatter "logging.Formatter")。如果您希望通过配置执行此操作，则可以使用[`dictConfig()`](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig "logging.config.dictConfig")以下完整示例所示的方法使用API：

```python
import logging
import logging.config
import time

class UTCFormatter(logging.Formatter):
    converter = time.gmtime

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'utc': {
            '()': UTCFormatter,
            'format': '%(asctime)s  %(message)s',
        },
        'local': {
            'format': '%(asctime)s  %(message)s',
        }
    },
    'handlers': {
        'console1': {
            'class': 'logging.StreamHandler',
            'formatter': 'utc',
        },
        'console2': {
            'class': 'logging.StreamHandler',
            'formatter': 'local',
        },
    },
    'root': {
        'handlers': ['console1', 'console2'],
   }
}

if __name__ == '__main__':
    logging.config.dictConfig(LOGGING)
    logging.warning('The local time is %s', time.asctime())
```

运行此脚本时，它应该打印如下：

```
2015-10-17 12:53:29,501 The local time is Sat Oct 17 13:53:29 2015
2015-10-17 13:53:29,501 The local time is Sat Oct 17 13:53:29 2015
```

显示时间如何格式化为本地时间和UTC，每个处理程序一个。

### 使用上下文管理器进行选择性记录

有时暂时更改日志记录配置并在执行某些操作后将其还原为有用。为此，上下文管理器是保存和恢复日志记录上下文的最明显方式。下面是一个这样的上下文管理器的简单示例，它允许您可选地更改日志记录级别并仅在上下文管理器的范围内添加日志记录处理程序：

```python
import logging
import sys

class LoggingContext(object):
    def __init__(self, logger, level=None, handler=None, close=True):
        self.logger = logger
        self.level = level
        self.handler = handler
        self.close = close

    def __enter__(self):
        if self.level is not None:
            self.old_level = self.logger.level
            self.logger.setLevel(self.level)
        if self.handler:
            self.logger.addHandler(self.handler)

    def __exit__(self, et, ev, tb):
        if self.level is not None:
            self.logger.setLevel(self.old_level)
        if self.handler:
            self.logger.removeHandler(self.handler)
        if self.handler and self.close:
            self.handler.close()
        # implicit return of None => don't swallow exceptions
```

如果指定级别值，则记录器的级别将设置为上下文管理器涵盖的with块范围内的值。如果指定了一个处理程序，它将在进入块时添加到记录器中，并在从块退出时删除。您还可以要求管理器在块退出时为您关闭处理程序 - 如果您不再需要处理程序，则可以执行此操作。

为了说明它是如何工作的，我们可以在上面添加以下代码块：

```python
if __name__ == '__main__':
    logger = logging.getLogger('foo')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)
    logger.info('1\. This should appear just once on stderr.')
    logger.debug('2\. This should not appear.')
    with LoggingContext(logger, level=logging.DEBUG):
        logger.debug('3\. This should appear once on stderr.')
    logger.debug('4\. This should not appear.')
    h = logging.StreamHandler(sys.stdout)
    with LoggingContext(logger, level=logging.DEBUG, handler=h, close=True):
        logger.debug('5\. This should appear twice - once on stderr and once on stdout.')
    logger.info('6\. This should appear just once on stderr.')
    logger.debug('7\. This should not appear.')
```

我们最初将记录器的级别设置为`INFO`，因此显示消息＃1而消息＃2不显示。然后我们将级别更改为`DEBUG`临时在下一个`with`块中，因此会显示消息＃3。块退出后，记录器的级别将恢复到`INFO`，因此不会显示消息＃4。在下一个`with`块中，我们`DEBUG`再次设置级别，但也添加一个写入的处理程序`sys.stdout`。因此，消息＃5在控制台上出现两次(一次通过`stderr`，一次通过`stdout`)。在`with`语句完成之后，状态就像之前一样，因此消息＃6出现(如消息＃1)，而消息＃7则不然(就像消息＃2一样)。

如果我们运行生成的脚本，结果如​​下：

```python
$ python logctx.py
1. This should appear just once on stderr.
2. This should appear once on stderr.
3. This should appear twice - once on stderr and once on stdout.
4. This should appear twice - once on stderr and once on stdout.
5. This should appear just once on stderr.
```

如果我们再次运行它，但管`stderr`到`/dev/null`，我们看下面的，这是写入唯一的消息`stdout`：

```python
$ python logctx.py 2>/dev/null
5. This should appear twice - once on stderr and once on stdout.
```

再一次，但管道`stdout`来`/dev/null`，我们得到：

```python
$ python logctx.py >/dev/null
1. This should appear just once on stderr.
3. This should appear once on stderr.
5. This should appear twice - once on stderr and once on stdout.
6. This should appear just once on stderr.
```

在这种情况下，打印的消息＃5 `stdout`没有出现，如预期的那样。

当然，这里描述的方法可以概括，例如临时附加日志记录过滤器。请注意，上面的代码适用于Python 2以及Python 3。
