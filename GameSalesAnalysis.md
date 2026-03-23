# 游戏销量分布分析报告

## 一、报告摘要

报告基于包含 16598 条视频游戏销售记录的数据集（来源：Kaggle，筛选条件为销量超 10 万份），从销量分布、游戏类型、发布平台、发行年份、发行商等维度展开分析，想要挖掘游戏销量的核心特征与关键影响因素，可为游戏发行策略、广告投放方向提供一些数据支撑，有以下要点：

游戏全球销量呈现极度右偏分布，头部效应显著；

动作类游戏发行数量最多，体育类游戏总销量最高；

任天堂旗下平台（Wii、NES 等）在销量排名中表现突出；

欧美游戏市场相对互通，日本市场相对独立；

2006 年诞生了全球销量最高的游戏，2000 年前后是游戏爆款集中诞生期。

## 二、数据概述

### 2.1 数据来源

数据集来自 Kaggle（https://www.kaggle.com/datasets/gregorut/videogamesales）

### 2.2 数据结构

数据集共 11 个字段、原始 16598 行记录

|   英文字段   |          中文释义          |        数据类型        |
| :----------: | :------------------------: | :--------------------: |
|     Rank     |        总销售额排名        |          整型          |
|     Name     |          游戏名称          |         字符串         |
|   Platform   |        游戏发布平台        |         字符串         |
|     Year     |        游戏发行年份        | 浮点型（后转换为整型） |
|    Genre     |          游戏类型          |         字符串         |
|  Publisher   |         游戏出版者         |         字符串         |
|   NA_Sales   |     北美销售额（百万）     |         浮点型         |
|   EU_Sales   |     欧洲销售额（百万）     |         浮点型         |
|   JP_Sales   |     日本销售额（百万）     |         浮点型         |
| Other_Sales  | 世界其他地区销售额（百万） |         浮点型         |
| Global_Sales |    全球销售总额（百万）    |         浮点型         |

### 2.3 基础统计

- 唯一游戏名称：11493 个

- 唯一发布平台：31 个

- 唯一游戏类型：12 类

- 唯一发行商：578 家

  ![image-20260323090512704](C:\Users\20677\Desktop\游戏数据集\assets\image-20260323090512704-1774227944016-2.png)

## 三、数据预处理

### 3.1 缺失值处理

原始数据存在少量缺失值：

- 年份（Year）缺失 271 条，占比 1.63%
- 发行商（Publisher）缺失 58 条，占比 0.35%
- 其余字段无缺失值

处理方式：删除所有含缺失值的记录，最终保留 16291 条有效记录。

### 3.2 异常值分析

通过箱线图分析全球销量（Global_Sales），直观呈现销量分布特征：

#### 图表 3-1：游戏全球销量箱线图（左：全量区间；右：0-5 百万区间）

![img](C:\Users\20677\Desktop\游戏数据集\assets\result_14_1.png)

- 核心特征：游戏全球销量呈**极度右偏分布**，绝大多数游戏销量集中在 0 附近，仅极少数爆款游戏销量极高，头部效应显著；

#### 表 3-2：游戏数据集各数值字段相关性热力图

分析：

**全球销量**：全球销量（Global_Sales）与北美销量（NA_Sales）相关系数 0.94，与欧洲销量（EU_Sales）0.90，呈极强正相关，说明北美、欧洲是全球销量的主要市场，欧美市场的爆款天然具备全球爆款的潜力；

**区域关联性**：北美与欧洲销量相关系数 0.77，呈强正相关，两大市场用户偏好高度趋同；日本销量（JP_Sales）与其他地区销量相关系数均低于 0.5，与欧美市场相关性极弱，用户偏好高度独立，与全球市场形成明显割裂；

**年份影响**：发行年份（Year）与所有销量字段相关系数绝对值均低于 0.2，说明发行时间对游戏销量的影响极小，游戏销量核心取决于产品质量、IP、类型、发行商等因素，发行早晚比重不大。

### 3.3 数据类型转换

将 “Year” 字段从浮点型转换为整型（先四舍五入再转换为 datetime 后提取年份），便于年份维度的分析。

## 四、多维度分析

### 4.1 游戏类型维度分析

#### （1）发行数量

动作类（Action）游戏发行数量最多（3251 款），其次是体育类（Sports，2304 款）、杂项类（Misc，1686 款）；解谜类（Puzzle）发行数量最少（570 款）。

#### 图表 4-1：不同游戏类型发行个数占比矩形树图

![result_19_4](C:\Users\20677\Desktop\游戏数据集\assets\result_19_4.png)

- 说明：矩形面积与发行数量正相关，颜色采用浅橙 - 浅黄色系渐变，直观呈现各类型发行规模差异；
- 分析：动作类、体育类是发行数量第一梯队，解谜类、策略类发行规模最小。

#### （2）销量表现

#### 图表 4-2：游戏类型销量柱状图（上：全周期；下：近五年）

![result_21_9](C:\Users\20677\Desktop\游戏数据集\assets\result_21_9.png)

- 全周期：体育类游戏总销量最高，动作类、射击类（Shooter）紧随其后；
- 近五年：射击类、动作类游戏销量增长显著，成为主流热门类型；

- 说明：采用橙黄色系渐变配色，柱状高度对应销量（单位：百万），标注具体销量数值；
- 分析：全周期体育类销量断层领先，近五年射击类反超成为第一，动作类稳居第二。

#### （3）历史最好排名

体育类游戏排名第 1（Wii Sports），平台类（Platform）第 2，竞速类（Racing）第 3；策略类（Strategy）游戏最好排名仅 166 位，表现最弱。

#### 图表 4-3：各游戏类型历史最好排名棒棒糖图

![result_24_20](C:\Users\20677\Desktop\游戏数据集\assets\result_24_20-1774228197819-10.png)

- 说明：横向条形长度对应排名（数值越小排名越优），标注具体排名，添加 Top10/Top50 参考线；
- 分析：体育、平台、竞速类占据头部位置，策略类是唯一未进入 Top50 的类型。

### 4.2 游戏平台维度分析

#### （1）销量表现

- 全周期：Wii、PS2、X360 等平台总销量领先，其中 Wii 平台销量断层式领先；
- 近五年：PS4、XOne 等新一代主机销量崛起，传统经典平台（如 Wii、NES）销量下滑。

#### 图表 4-4：游戏平台销量柱状图（上：全周期；下：近五年）

![result_25_9](C:\Users\20677\Desktop\游戏数据集\assets\result_25_9.png)

- 说明：筛选销量＞1 百万的平台，橙黄色系渐变配色，标注具体销量数值；
- 分析：全周期 Wii 平台销量碾压式领先，近五年 PS4、XOne 成为主流，经典平台销量大幅下滑。

#### （2）历史最好排名

任天堂旗下平台占据绝对优势：

- Wii 平台排名第 1（对应游戏 Wii Sports），NES 第 2，GB 第 5；
- 小众平台（如 PCFX、GG、3DO）最好排名均在万位以后，市场表现极差。

### 4.3 发行年份维度分析

#### （1）发行数量趋势

游戏发行数量在 2000-2010 年达到峰值，2010 年后发行数量逐步下降。

#### 图表 4-5：每年发行游戏数量趋势柱状图

![result_30_0](C:\Users\20677\Desktop\游戏数据集\assets\result_30_0.png)

- 说明：横轴为年份，纵轴为发行数量，红色柱状呈现趋势变化；
- 分析：2000-2010 年是游戏发行黄金期，2008 年左右达到发行峰值，此后逐年下降。

#### （2）销量排名

- 2006 年诞生了全球销量最高的游戏（Wii Sports），1985 年（Super Mario Bros.）、2008 年（Mario Kart Wii）、2009 年（Wii Sports Resort）紧随其后；
- 爆款游戏集中诞生于 2000 年前后，2010 年后无顶级爆款（排名前 10 的游戏均诞生于 2010 年前）。

### 4.4 全球市场商维度分析

#### （1）全球市场发展趋势

#### 图表 4-6：五大市场发展趋势折线图

![result_34_1](C:\Users\20677\Desktop\游戏数据集\assets\result_34_1.png)

**分析：**

**整体周期**：全球销量（Global_Sales）走势与北美、欧洲市场高度同步，2008 年左右达到历史峰值（近 700 百万），2010 年后持续下滑，与游戏发行数量、主机代际更替趋势完全一致；

**核心市场**：北美市场（NA_Sales）长期是全球第一大消费市场，峰值出现在 2008-2010 年，最高超 350 百万，贡献了全球近 40% 的销量，是全球游戏市场的基本盘；

**增长市场**：欧洲市场（EU_Sales）增长趋势与北美高度一致，峰值略晚于北美，2010 年左右达到近 200 百万，成为全球第二大市场，是游戏全球化发行的增量市场；

**独立市场**：日本市场（JP_Sales）走势完全独立，增长平稳，无爆发式增长，峰值出现在 1995 年左右，此后长期稳定在 50-80 百万区间，2010 年后缓慢下滑，与欧美市场的爆发 - 下滑周期不同；

**新兴市场**：其他地区（Other_Sales）随全球市场同步增长，2010 年左右达到峰值，成为增量市场。

#### 图表 4-7：各地区游戏类型销量占比堆叠条形图

![result_45_5](C:\Users\20677\Desktop\游戏数据集\assets\result_45_5.png)

**分析：**

**二元市场格局**：全球游戏市场呈现 **“欧美趋同、日本独立”** 的核心特征：

- 北美、欧洲、其他地区的类型偏好高度一致，为「动作 + 体育 + 射击」，三大类型合计占比均超 45%。
- 日本市场差异化，角色扮演类（RPG）以 27.3% 的占比成为绝对核心，是欧美市场的 3 倍以上，而射击类占比仅 3.0%，不足欧美市场的 1/4，形成了市场壁垒。

**全区域通用品类**：动作类（Action）是唯一在所有地区均进入销量占比前三的品类，；体育类（Sports）在欧美稳居第二，在日本也进入前五。

**区域专属红利品类**：射击类（Shooter）是欧美市场的专属，在北美、欧洲占比均超 12%，但在日本市场表现极差；RPG 是日本市场的壁垒，也是唯一能在日本市场突破 20% 占比的品类，是深耕日本市场的核心赛道。

**小众品类生存空间**：解谜、冒险、策略等小众类型在日本市场的占比显著高于欧美，在日本具备更好的生存土壤，在欧美市场则被主流品类严重挤压。

### 4.5 发行商维度分析

#### 4.5.1 头部发行商发展趋势

#### 图表 4-8：五大发行商的市场发展趋势折线图

![result_38_0](C:\Users\20677\Desktop\游戏数据集\assets\result_38_0.png)

**分析：**

1. **任天堂**：任天堂（Nintendo）的销量走势呈现极强的***爆发性***，2006 年、2009 年两次出现销量峰值，最高超 200 百万，远超其他厂商，核心得益于 Wii 平台爆款游戏的集中爆发，主机与内容形成了极强的双向赋能；
2. **EA **：艺电（Electronic Arts，EA）的增长最为***平稳***，1995 年后持续增长，2008-2010 年达到峰值，无剧烈波动，凭借《FIFA》《Madden NFL》等体育年货 IP 的稳定迭代，实现了穿越周期的销量韧性；
3. **第三方厂商**：动视（Activision）、育碧（Ubisoft）、索尼电脑娱乐（Sony Computer Entertainment）在 2000 年后进入***增长快车道***，2005-2010 年达到峰值，与主机市场的爆发周期高度同步，凭借跨平台发行策略实现了快速增长；
4. **后黄金期**：2010 年后，所有头部厂商的销量均出现不同程度的下滑，任天堂的下滑幅度最大，主机绑定的模式受代际更替影响显著；而 EA、动视的下滑相对平缓，跨平台、多 IP 运营的模式抗风险能力显著更强。

#### 4.5.2 发行商市场格局演变

#### 图表 4-9：发行商全球销量占比：全时段 vs 近十年 饼图

![result_39_1](C:\Users\20677\Desktop\游戏数据集\assets\result_39_1.png)

**分析：**

1. **全时段格局：任天堂一家独大**：全周期维度，任天堂以 20.3% 的占比断层领先，远超第二名 EA（12.4%），Top8 厂商合计占比 64.7%，中小发行商合计占比 35.3%，头部效应显著，任天堂凭借主机与 IP 的双重优势，统治了游戏行业近 40 年的发展历程。
2. **近十年格局：多强发展**：近十年行业格局发生根本性逆转，任天堂的统治地位大幅下滑，占比降至 12.5%；EA 以 14.6% 的占比跃居第一，动视（12.1%）、育碧（9.2%）紧随其后，形成「EA 领衔、多强鼎立」的均衡格局。
3. **马太效应加剧**：近十年 Top8 厂商合计占比 69.6%，较全时段提升 4.9 个百分点，中小发行商占比降至 30.4%，说明行业向头部大厂进一步集中，精品化、规模化的行业趋势下，中小发行商的生存空间被持续挤压。
4. **格局动态变化**：华纳兄弟、万代南梦宫等新玩家进入近十年 Top8，而全时段 Top8 的 THQ、科乐美则掉出榜单，体现了行业核心竞争力的转变：从「主机绑定」转向「跨平台 IP 运营」，具备高频次 IP 迭代、全平台发行能力的厂商，成为行业新的领导者。

#### 4.5.3 头部厂商专精赛道分析

#### 图表 4-10：五大厂商 - 游戏类型销量热力图（全局概览）![result_44_4](C:\Users\20677\Desktop\游戏数据集\assets\result_44_4.png)

#### 图表 4-11：五大厂商各游戏类型全球销量对比水平条形图

![result_41_5](C:\Users\20677\Desktop\游戏数据集\assets\result_41_5.png)

**分析：**

头部厂商形成了高度差异化的专精赛道，赛道壁垒极强，行业无全面同质化竞争，而是形成了互补的市场格局：

1. **艺电（EA）：体育赛道TOP1**：体育类总销量 468.7 百万，远超其他所有厂商同类型销量之和，是该赛道的绝对统治者，同时在射击、竞速类也具备较强竞争力，形成了 “体育为核心，多赛道补充” 的布局；
2. **动视（Activision）：射击赛道TOP1**：射击类总销量 295.4 百万，是该赛道的绝对头部，凭借《使命召唤》等超级 IP，形成了极强的用户粘性，是欧美射击市场的核心供应商；
3. **育碧（Ubisoft）：动作赛TOP1**：动作类总销量 142.9 百万，位列五大厂商第一，在冒险、模拟类也有稳定表现，凭借开放世界动作 IP，形成了独特的赛道优势；
4. **任天堂（Nintendo）：全类型布局**：统治平台类、角色扮演类（RPG）赛道，平台类销量 426.2 百万、RPG 类 284.6 百万，均为全行业第一，同时在体育、竞速、解谜类也具备极强的竞争力，是唯一全赛道均有布局且多赛道领先的厂商，核心优势在于自有 IP 与主机平台的深度绑定；
5. **索尼电脑娱乐：主机平台核心内容供应商**：在平台、竞速类具备较强竞争力，核心服务于索尼 PlayStation 主机生态，是主机平台独占内容的核心产出方。
6. **中小厂商生存空间**：五大厂商在冒险、解谜、策略类的布局均较弱，这些小众赛道是中小发行商的差异化生存空间，可避开与头部大厂的直接竞争。

#### 4.5.4 头部厂商区域市场布局

#### 图表 4-12：五大厂商各地区总销量分布柱状图

![result_46_5](C:\Users\20677\Desktop\游戏数据集\assets\result_46_5.png)

**分析：**

1. **北美市场：全厂商**：北美市场是所有头部厂商的第一大收入来源，任天堂在北美市场销量 815.8 百万，位列第一，动视 426.0 百万、EA584.2 百万紧随其后，北美市场贡献了头部厂商近 50% 的总销量，是全球化发行的必争之地；
2. **日本市场：任天堂**：任天堂在日本市场销量 455.0 百万，远超其他四大厂商之和，其他厂商在日本市场的销量均不足 80 百万，体现了任天堂在本土市场的绝对统治力，海外厂商难以突破日本市场的本土壁垒；
3. **欧洲市场：EA **：EA 在欧洲市场销量 367.4 百万，位列第一，任天堂 418.3 百万紧随其后，动视、育碧在欧洲市场也有稳定的销量贡献，欧洲市场是仅次于北美的第二大全球化市场；
4. **其他地区：全球化能力的试金石**：EA、任天堂、索尼在其他地区市场销量领先，体现了其成熟的全球化布局能力，而动视、育碧在新兴市场的布局相对较弱。

## 五、分析

1. **销量分布特征**：游戏行业呈现 “头部效应极致化” 特征，少数爆款贡献绝大多数销量，长尾游戏销量普遍偏低；
2. **类型偏好**：动作类游戏发行数量最多，体育类全周期销量最高，近五年射击类、动作类成为新增长点，策略类、解谜类表现弱势；
3. **平台格局**：任天堂系平台（Wii、NES 等）是经典爆款的核心载体，新一代主机（PS4、XOne）逐步接棒主流市场；
4. **时间特征**：2000-2010 年是游戏发行与爆款诞生的黄金期，2010 年后发行数量与顶级爆款产出均下滑；
5. **发行商壁垒**：任天堂占据绝对头部地位，中小发行商难以突破头部发行商的市场垄断。
6. **销量核心影响因素**：游戏销量核心取决于产品类型、IP、发行商、平台，发行年份对销量的影响极弱；北美、欧洲市场销量与全球销量高度相关，是全球核心市场，日本市场相对独立。

## 六、业务建议

### 6.1 产品研发

- 优先布局动作类、射击类等当下热门类型，兼顾体育类经典高销量类型；
- 策略类、解谜类游戏需差异化创新，避免同质化竞争。

### 6.2 平台选择

- 主流市场聚焦 PS4、XOne 等新一代主机，同时可挖掘任天堂平台的经典 IP 合作机会；
- 放弃小众平台（如 PCFX、GG）的资源投入。

### 6.3 营销投放

- 针对长尾游戏：采用低预算、精准化投放策略，聚焦细分用户群体；
- 针对爆款游戏：加大投放力度，强化品牌认知，最大化生命周期价值（LTV）；
- 重点布局 2000-2010 年经典 IP 的复刻 / 续作营销，利用怀旧情绪提升销量。

### 6.4 发行合作

- 优先与任天堂、微软、索尼等头部发行商合作，获取优质 IP 与渠道资源；
- 对中小发行商，聚焦其细分领域的特色游戏，低成本孵化潜力产品。

---

```python
"""
py代码是在Jupyter Notebook上面按代码块跑的，此为整合代码
"""

import squarify
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
#%matplotlib inline

# 杂项配置
warnings.simplefilter(action="ignore", category=FutureWarning) # 警告忽略
from IPython.display import display_html
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all" # 结果都显示出来

pd.set_option('max_colwidth', 200) # 控制单元格最大显示宽度
pd.set_option('display.max_columns', 40)  # 控制显示最大的列数

plt.rcParams['font.sans-serif']=['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False  # 用来正常显示负号

html = f"""
<html>
<head>
    <style>
        div{{
            background-color: rgba(255, 106, 106, 0.01); /* 包裹表格的 div 背景色 */
        }}
        th{{
            background-color: #FF6A6A; /* 表头背景色 */
            color: black; /* 表头文字颜色 */
        }}
    </style>
</head>
</html>
"""
display_html(html, raw=True)

df = pd.read_csv('vgsales.csv') #加载数据集
df.head(10)
df.info()
# 与下面做对照
df.shape

def show_unique(df: pd.DataFrame, col_list: list) -> pd.DataFrame:
    """
    批量统计DataFrame多列的唯一值/唯一值数量

    参数：
        df (pd.DataFrame)：待分析的数据框
        col_list (list)：列名列表，以'N'结尾的列名对应统计原列唯一值数量

    返回：
        pd.DataFrame：转置后的结果，行=列名，列=唯一值/数量

    示例：
        show_unique(df, ['Platform', 'PlatformN', 'Genre'])
    """
    # 初始化字典
    unique_dict = {}

    for col in col_list:
        # 处理列名不存在的情况
        if col not in df.columns and not (col[:-1] in df.columns and col.endswith('N')):
            unique_dict[col] = ['列名不存在']
            continue

        if col.endswith('N'):
            # 提取原列名
            original_col = col[:-1]
            # 统计唯一值数量（列表包裹）
            unique_count = [df[original_col].nunique()]
            unique_dict[col] = unique_count
        else:
            # 提取唯一值并转为列表（方便补全空白）
            unique_vals = df[col].unique().tolist()
            unique_dict[col] = unique_vals

    # 计算最大长度
    if not unique_dict:
        return pd.DataFrame()
    max_len = max(len(v) for v in unique_dict.values())

    # 补全空白，对齐数据
    for key, vals in unique_dict.items():
        if len(vals) < max_len:
            unique_dict[key] = vals + [''] * (max_len - len(vals))  # 用空字符串更规范

    # 转置后返回
    return pd.DataFrame(unique_dict)

li = ['Platform', 'Genre', 'NameN','PlatformN','GenreN','PublisherN']
show_unique(df, li).T

df.boxplot(column='Global_Sales')
plt.show()

df.boxplot(column='Global_Sales')
plt.ylim(0, 5)  # 只看 0~5 的销量区间
plt.show()

def missing (df):
    """
    计算每一列的缺失值及占比
    """
    missing_number = df.isnull().sum().sort_values(ascending=False)              # 每一列的缺失值求和后降序排序
    missing_percent = (df.isnull().sum()/df.isnull().count()).sort_values(ascending=False)          # 每一列缺失值占比
    missing_values = pd.concat([missing_number, missing_percent], axis=1, keys=['Missing_Number', 'Missing_Percent'])      # 合并为一个DataFrame
    return missing_values

# 查看数值列的异常值
df.boxplot(column='Global_Sales')  # 查看全球销量的异常值
plt.show()

missing(df).T

# 转换年份数据类型
df['Year'] = pd.to_datetime(df['Year'].round().astype(int), format='%Y').dt.year
df.sample()

genre_counts = df['Genre'].value_counts().sort_values(ascending=False)
labels = genre_counts.index.tolist()
sizes = genre_counts.values.tolist()

# 选择橙色系色板（Oranges）
cmap = plt.colormaps['Oranges']
# 生成颜色区间：0.2（浅黄）→ 0.8（浅橙），避开深色区间
colors = cmap(np.linspace(0.1, 0.7, len(labels)))
# 反转颜色：让数量多的区块浅橙，数量少浅黄色
colors = colors[::-1]

# 绘图
plt.figure(figsize=(14, 8), dpi=120)

squarify.plot(
    sizes=sizes,
    label=labels,
    color=colors,
    alpha=0.9,
    text_kwargs={'fontsize': 18, 'weight': 'bold'}
)

# 美化
plt.title('不同游戏类型发行游戏个数占比情况', fontsize=14, pad=20)
plt.axis('off')
plt.tight_layout()

plt.show()

# 发行个数
df.Genre.value_counts().to_frame().T

# 图形绘制数据标签函数
def add_labels(ax, data):
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(f'{height:.0f}',
                        xy=(p.get_x() + p.get_width() / 2, height),
                        xytext=(0, 6),
                        textcoords="offset points",
                        ha='center', va='bottom')

# 数据处理
LoveG = pd.pivot_table(df, index='Year', columns='Genre', values='Global_Sales', aggfunc=np.sum).sum().sort_values(ascending=False)
LoveG = pd.DataFrame(data=LoveG, columns=['Genre_sales'])

LoveG5 = pd.pivot_table(df, index='Year', columns='Genre', values='Global_Sales', aggfunc=np.sum).iloc[-5:,:].sum().sort_values(ascending=False)
LoveG5 = pd.DataFrame(data=LoveG5, columns=['Genre_sales'])


# as_cmap=False 确保返回的是列表格式，适配 barplot
palette = sns.color_palette("YlOrBr", n_colors=len(LoveG))

# 绘图
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), dpi=120)
plt.subplots_adjust(hspace=0.4, top=0.92, bottom=0.08)

# 绘图
sns.barplot(x=LoveG.index, y='Genre_sales', data=LoveG, ax=ax1, palette=palette, hue=LoveG.index, legend=False)
add_labels(ax1, LoveG['Genre_sales'])

# 第二个子图截取对应长度的调色板即可
sns.barplot(x=LoveG5.index, y='Genre_sales', data=LoveG5, ax=ax2, palette=palette[:len(LoveG5)], hue=LoveG5.index, legend=False)
add_labels(ax2, LoveG5['Genre_sales'])

# 标题
ax1.set_title('全部年份各游戏类型销量情况')
ax1.set_xlabel('游戏类型')
ax1.set_ylabel('全球销量')

ax2.set_title('最近五年各游戏类型销量情况')
ax2.set_xlabel('游戏类型')
ax2.set_ylabel('全球销量')

fig.suptitle('全球游戏总销量按类型与年份的分布情况', fontsize=12)
plt.show()

#不同类型游戏的最好排名

df.groupby('Genre')['Rank'].min().to_frame().sort_values(by=['Rank']).T

#棒棒糖图可视化
genre_best_rank = df.groupby('Genre')['Rank'].min().sort_values(ascending=True)
rank_df = genre_best_rank.reset_index()
rank_df.columns = ['Genre', 'Best_Rank']


#配色
cmap = plt.colormaps['Oranges']
colors = cmap(np.linspace(0.25, 0.75, len(rank_df)))

# 反转颜色顺序：让排名越好（越靠上）的条形颜色lve深
colors = colors[::-1]

# 绘图
plt.figure(figsize=(10, 7), dpi=120)

ax = sns.barplot(
    data=rank_df,
    y='Genre',
    x='Best_Rank',
    palette=colors,
    hue='Genre',
    legend=False
)

# 添加数据标签
for p in ax.patches:
    rank_value = p.get_width()
    ax.annotate(
        f'第 {rank_value} 名',
        xy=(rank_value, p.get_y() + p.get_height()/2),
        xytext=(8, 0),
        textcoords='offset points',
        va='center',
        fontsize=9
    )

# 添加参考线
ax.axvline(x=10, color='#ff6b6b', linestyle='--', alpha=0.7, label='Top10门槛')
ax.axvline(x=50, color='#ffa502', linestyle='--', alpha=0.7, label='Top50门槛')
ax.legend(loc='lower right')

# 标题与坐标轴
ax.set_title('各游戏类型历史最好排名对比', fontsize=14, pad=15)
ax.set_xlabel('全榜排名（数值越小越好）', fontsize=11)
ax.set_ylabel('游戏类型', fontsize=11)

plt.tight_layout()
plt.show()

def add_labels(ax, data):
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(f'{height:.1f}',
                        xy=(p.get_x() + p.get_width() / 2, height),
                        xytext=(0, 6),
                        textcoords="offset points",
                        ha='center', va='bottom')

LoveP = pd.pivot_table(df, index='Year', columns='Platform', values='Global_Sales', aggfunc=np.sum).sum().sort_values(ascending=False)
LoveP = pd.DataFrame(data=LoveP, columns=['Platform_sales'])
LoveP = LoveP[LoveP['Platform_sales'] > 1]

LoveP5 = pd.pivot_table(df, index='Year', columns='Platform', values='Global_Sales', aggfunc=np.sum).iloc[-5:,:].sum().sort_values(ascending=False)
LoveP5 = pd.DataFrame(data=LoveP5, columns=['Platform_sales'])
LoveP5 = LoveP5[LoveP5['Platform_sales'] > 1]


cmap = plt.colormaps['Oranges']

colors = cmap(np.linspace(0.25, 0.75, len(LoveP))).tolist()  # <--- 这里加了 .tolist()
colors = colors[::-1]


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), dpi=120)
plt.subplots_adjust(hspace=0.4, top=0.92, bottom=0.08)


sns.barplot(x=LoveP.index, y='Platform_sales', data=LoveP, ax=ax1, palette=colors, hue=LoveP.index, legend=False)
add_labels(ax1, LoveP['Platform_sales'])

sns.barplot(x=LoveP5.index, y='Platform_sales', data=LoveP5, ax=ax2, palette=colors[:len(LoveP5)], hue=LoveP5.index, legend=False)
add_labels(ax2, LoveP5['Platform_sales'])

ax1.set_title('全部年份各游戏平台销量情况')
ax1.set_xlabel('游戏平台 (Platform)')
ax1.set_ylabel('全球销量 (单位: 百万)')

ax2.set_title('最近五年各游戏平台销量情况')
ax2.set_xlabel('游戏平台 (Platform)')
ax2.set_ylabel('全球销量 (单位: 百万)')

fig.suptitle('全球总游戏销量在发布平台及年份的情况', fontsize=12)
plt.show()

#不同游戏平台最好排名
#还得是任天堂，Wii与任天堂确实形成了极强的双向促进关系

df.groupby('Platform')['Rank'].min().to_frame().sort_values(by='Rank').T

#不同年份最好排名
#感觉没太大关系，但是基本集中在2000年附近了，现在游戏销量不如之前

df.groupby('Year')['Rank'].min().to_frame().sort_values(by='Rank').T
#%%
_ = df.Year.value_counts().plot(kind='bar',figsize=(21,8),color='r')
_=plt.title('每年发行的游戏数据量趋势',fontsize=28)
_=plt.xlabel('年份',fontsize=20)
_=plt.ylabel('游戏个数',fontsize=20)

#游戏厂商分析

#

df.groupby('Publisher')['Rank'].min().to_frame().sort_values(by='Rank').T

M=['NA_Sales','EU_Sales','JP_Sales','Other_Sales','Global_Sales']
#绘各销量走势图
DM=pd.pivot_table(df,index='Year',values=M,aggfunc=np.sum)
fig=plt.figure(figsize=(12,6),dpi=120)
DM.T
_=sns.lineplot(data=DM)
_=plt.title('五大市场发展趋势',fontsize=18)
_=plt.xlabel('年份')
_=plt.ylabel('销售额')

#相关性分析
#欧美相关性强，游戏爆款互通,日本相对独立
#欧美跟全球市场相关性强，一个说明全球市场中欧美占比大，另一个是
#销量越高 RANK越小
#游戏发行年份无太多影响，主要跟质量，IP有关

matrix = df.corr(numeric_only=True)
fig = plt.figure(figsize=(10, 8), dpi=120)
_ = sns.heatmap(
    matrix,
    annot=True,        # 显示相关系数数值
    cmap='coolwarm',   # 配色：蓝-白-红，正相关红，负相关蓝，比默认配色更直观
    vmin=-1, vmax=1,  # 颜色范围固定在 -1 到 1
    fmt='.2f',        # 数值保留两位小数
    linewidths=0.5    # 增加网格线
)
plt.title('游戏数据集各数值字段相关性热力图', fontsize=14, pad=15)
plt.show()

"""
发行商分析
2005-2010左右销量均暴增，但是后面下滑严重且五大厂商差距很小
"""

P=['Nintendo','Electronic Arts','Activision','Sony Computer Entertainment','Ubisoft']
DP=df[df['Publisher'].isin(P)]
DP_=pd.pivot_table(data=DP,index='Year',columns='Publisher',values='Global_Sales',aggfunc=np.sum)
_=DP_.plot(figsize=(25,10),fontsize=18)
_=plt.title('五大发行商的市场发展趋势',fontsize=28)
_=plt.xlabel('年份',fontsize=20)
_=plt.ylabel('销售额',fontsize=20)
_=plt.legend(fontsize=20)

def draw_pie_chart(ax, pie_data, title, colors):
    """
    绘制饼图的通用函数
    :param ax: 子图对象
    :param pie_data: 饼图数据（Series）
    :param title: 子图标题
    :param colors: 配色列表
    """
    wedges, texts, autotexts = ax.pie(
        pie_data,
        labels=pie_data.index,
        colors=colors,
        autopct='%1.1f%%',         # 百分比保留1位小数
        startangle=90,             # 起始角度90°
        textprops={'fontsize': 9}, # 标签字号（子图需缩小）
        wedgeprops={
            'edgecolor': 'white',
            'linewidth': 1.2
        },
        pctdistance=0.85
    )
    # 美化百分比文字
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_weight('bold')
        autotext.set_fontsize(8)
    # 设置子图标题
    ax.set_title(title, fontsize=12, pad=15)
    # 保证饼图为正圆形
    ax.axis('equal')


# 统计全时段各发行商销量总和并排序
publisher_sales_all = df.groupby('Publisher')['Global_Sales'].sum().sort_values(ascending=False)
# 取Top8 + 其他
top_n = 8
top_publishers_all = publisher_sales_all.head(top_n)
other_sales_all = publisher_sales_all.iloc[top_n:].sum()
pie_data_all = top_publishers_all._append(pd.Series([other_sales_all], index=['其他']))


# 筛选近十年数据（自动适配最新年份）
max_year = df['Year'].max()
start_year = max_year - 9
recent_10y_data = df[df['Year'] >= start_year]
# 统计近十年销量总和并排序
publisher_sales_10y = recent_10y_data.groupby('Publisher')['Global_Sales'].sum().sort_values(ascending=False)
# 取Top8 + 其他
top_publishers_10y = publisher_sales_10y.head(top_n)
other_sales_10y = publisher_sales_10y.iloc[top_n:].sum()
pie_data_10y = top_publishers_10y._append(pd.Series([other_sales_10y], index=['其他']))


# 创建1行2列的子图布局，设置画布大小（宽屏适配双饼图）
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8), dpi=120)

# 统一配色（两个饼图用同一套色系，保证视觉协调）
colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC', '#99CCFF', '#FFB366', '#C2C2F0', '#E6E6FA']

# 绘制左图：全时段销量占比
draw_pie_chart(
    ax=ax1,
    pie_data=pie_data_all,
    title=f'全时段各发行商全球销量占比（Top 8 + 其他）',
    colors=colors
)

# 绘制右图：近十年销量占比
draw_pie_chart(
    ax=ax2,
    pie_data=pie_data_10y,
    title=f'近十年（{start_year}-{max_year}）各发行商全球销量占比（Top 8 + 其他）',
    colors=colors
)

# 总标题 + 布局调整
fig.suptitle('发行商全球销量占比：全时段 vs 近十年', fontsize=18, y=1.02)  # 总标题置顶，避免遮挡
plt.tight_layout(rect=[0, 0, 1, 0.98])  # 调整布局，给总标题留空间

plt.show()
print("===== 全时段销量明细（单位：百万份） =====")
print(pie_data_all.round(2))
print("\n===== 近十年销量明细（单位：百万份） =====")
print(pie_data_10y.round(2))
#%%
# 详细分布占比
DPG=pd.pivot_table(data=DP,index=['Genre','Publisher'],values=M,aggfunc=np.sum)
DPG.sort_values(by=['Genre','Global_Sales'],ascending=False)

"""
游戏发行商的市场格局发生了根本性逆转：核心格局从「任天堂单极独大」演变为「EA 领衔、多强鼎立」，市场集中度显著提升，中小发行商的生存空间被头部大厂挤压。具体表现为：任天堂统治地位大幅下滑，而 EA、动视、育碧等第三方厂商凭借跨平台策略强势崛起，成为近十年市场增长的核心动力
近十年行业逻辑已从 **「硬件驱动」转向「内容与跨平台驱动」**：头部厂商的竞争力不再依赖主机绑定，而是靠高频 IP 迭代、全平台覆盖和精细化运营；同时，市场向头部集中，印证了游戏行业「规模化、精品化」的核心趋势
近十年游戏发行商格局从「任天堂独大」转为「EA、动视、育碧三足鼎立」，任天堂份额大幅下滑，市场从硬件驱动转向内容，平台驱动

多维度对比:
1.五大厂商专精领域对比
动视吃定射击 IP，EA 吃定体育生态，任天堂吃定全年龄休闲
2.五大厂商各个地域对比
北美是销量天花板，日本是任天堂主场，欧洲是 EA 主场，五大厂商形成了高度差异化的「区域割据」格局
3.各地区游戏类型销量占比
全球游戏市场呈现 **「欧美趋同、日本独立」** 的二元格局：北美、欧洲和其他地区偏好高度一致，形成  **「动作 + 体育 + 射击」** 的主流基本盘；而日本市场则完全差异化，以 **「RPG」** 为绝对核心，和欧美市场形成鲜明割裂
通用型：Action（动作）和 Sports（体育）是全地区的核心类型，占比均进入前三，是跨区域发行的「通行证」；
区域型：Shooter（射击）是欧美专属红利（占比 12.9%~13.3%），但在日本仅 3.0%；而 RPG（角色扮演）是日本的绝对壁垒（占比 27.3%），在欧美仅 7.5%~7.8%；
小众型：解谜、冒险、策略等小众类型在日本占比更高，生存空间优于欧美
全球化布局优先押注Action/Sports；深耕欧美可加码Shooter/Racing；深耕日本必须聚焦RPG，同时兼顾 Action/Sports/Fighting 类，射击类可战略性放弃
"""

def add_labels(ax, is_horizontal=True):
    for p in ax.patches:
        if is_horizontal:
            # 水平条形图的标签
            width = p.get_width()
            if width > 0:
                ax.annotate(f'{width:.1f}',
                            xy=(width, p.get_y() + p.get_height()/2),
                            xytext=(5, 0),
                            textcoords='offset points',
                            va='center', fontsize=8)
        else:
            # 垂直柱状图的标签
            height = p.get_height()
            if height > 0:
                ax.annotate(f'{height:.1f}',
                            xy=(p.get_x() + p.get_width()/2, height),
                            xytext=(0, 5),
                            textcoords='offset points',
                            ha='center', fontsize=8)


# 重置多层索引，把Genre和Publisher从索引变成普通列
DPG = DPG.reset_index()

# 锁定分析的5家厂商
target_publishers = [
    'Nintendo',
    'Activision',
    'Electronic Arts',
    'Ubisoft',
    'Sony Computer Entertainment'
]

# 3. 过滤数据
DPG_filtered = DPG[DPG['Publisher'].isin(target_publishers)].copy()

# 4. 固定厂商配色
publisher_color_map = {
    'Nintendo': '#e63946',          # 任天堂-品牌红
    'Electronic Arts': '#ff9f1c',    # EA-品牌橙
    'Activision': '#1d3557',         # 动视-品牌蓝
    'Ubisoft': '#43aa8b',            # 育碧-品牌绿
    'Sony Computer Entertainment': '#560bad' # 索尼-品牌紫
}

# 厂商-类型销量热力图
# 数据预处理：「行=厂商，列=游戏类型，值=销量」的矩阵
heatmap_data = DPG_filtered.pivot_table(
    index='Publisher',
    columns='Genre',
    values='Global_Sales',
    aggfunc=np.sum,
    fill_value=0
)

#
plt.figure(figsize=(12, 5), dpi=120)

ax = sns.heatmap(
    heatmap_data,
    annot=True,        # 显示销量数值
    cmap='Oranges',    # 橙黄色渐变，颜色越深销量越高
    fmt='.0f',         # 不保留小数
    linewidths=0.5,
    vmin=0
)

ax.set_title('五大厂商-游戏类型销量热力图（全局概览）', fontsize=14, pad=15)
ax.set_xlabel('游戏类型', fontsize=11)
ax.set_ylabel('发行厂商', fontsize=11)

plt.tight_layout()
plt.show()

# 厂商-游戏类型 簇状水平条形图
plt.figure(figsize=(12, 10), dpi=120)

# 绘制簇状水平条形图
ax = sns.barplot(
    data=DPG_filtered,
    y='Genre',          # Y轴放游戏类型，保证长标签完整显示
    x='Global_Sales',   # X轴放全球总销量，对比厂商实力
    hue='Publisher',    # 按厂商分组，每个类型下分5个厂商的条形
    palette=publisher_color_map,  # 用固定的厂商配色
    # 按游戏类型总销量降序排列，把热门类型放在最上面
    order=DPG_filtered.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False).index
)

# 添加数据标签
add_labels(ax, is_horizontal=True)

# 图表美化
ax.set_title('五大厂商各游戏类型全球销量对比（看专精领域）', fontsize=14, pad=15)
ax.set_xlabel('全球总销量（单位：百万）', fontsize=11)
ax.set_ylabel('游戏类型', fontsize=11)
# 把图例放在图表外侧避免遮挡数据
ax.legend(title='发行厂商', bbox_to_anchor=(1.01, 1), loc='upper left')

plt.tight_layout()
plt.show()

# 分地区厂商销量堆叠柱状图
# 数据预处理：把宽表转成长表，适配分地区绘图
market_data = DPG_filtered.melt(
    id_vars=['Publisher'],
    value_vars=['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'], # 排除Global总和
    var_name='Market',
    value_name='Sales'
)
# 按地区+厂商聚合，计算每个地区各厂商的总销量
market_total = market_data.groupby(['Market', 'Publisher'])['Sales'].sum().reset_index()
market_total['Market'] = market_total['Market'].replace({
    'NA_Sales': '北美市场',
    'EU_Sales': '欧洲市场',
    'JP_Sales': '日本市场',
    'Other_Sales': '其他地区'
})

# 绘图
plt.figure(figsize=(10, 6), dpi=120)

ax = sns.barplot(
    data=market_total,
    x='Market',
    y='Sales',
    hue='Publisher',
    palette=publisher_color_map,

    # estimator=lambda x: x.sum() / x.sum() * 100
)

# 添加数据标签
add_labels(ax, is_horizontal=False)

# 图表美化
ax.set_title('五大厂商各地区总销量分布（看市场主导地位）', fontsize=14, pad=15)
ax.set_xlabel('销售地区', fontsize=11)
ax.set_ylabel('总销量（单位：百万）', fontsize=11)
ax.legend(title='发行厂商', bbox_to_anchor=(1.01, 1), loc='upper left')

plt.tight_layout()
plt.show()

regions = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']
region_labels = ['北美地区', '欧洲地区', '日本地区', '其他地区']
y_positions = np.arange(len(regions))  # 四个地区的y轴位置 [0,1,2,3]

# 存储每个地区的【降序类型列表】和【对应占比列表】
region_data = []
for region in regions:
    # 计算该地区各类型销量占比
    genre_sales = df.groupby('Genre')[region].sum()
    genre_pct = (genre_sales / df[region].sum() * 100).fillna(0)
    # 核心：按占比降序排序
    genre_pct_sorted = genre_pct.sort_values(ascending=False)
    region_data.append({
        "genres": genre_pct_sorted.index.tolist(),
        "values": genre_pct_sorted.values.tolist()
    })

genre_colors = {
    'Action': '#FF6B6B',
    'Sports': '#4ECDC4',
    'Misc': '#45B7D1',
    'Role-Playing': '#96CEB4',
    'Shooter': '#FECA57',
    'Platform': '#A55EEA',
    'Simulation': '#FF9FF3',
    'Racing': '#54A0FF',
    'Fighting': '#D3D3D3',
    'Adventure': '#FFE4E1',
    'Strategy': '#F0E68C',
    'Puzzle': '#E6E6FA'
}
# 兜底配色（防止有新类型）
default_color = '#CCCCCC'

# 绘图
fig, ax = plt.subplots(figsize=(18, 10), dpi=120)

# 遍历每个地区，逐个绘制自己的降序堆叠条形
for y_idx, data in enumerate(region_data):
    genres = data["genres"]
    values = data["values"]
    left = 0  # 每个地区从0开始堆叠
    for genre, val in zip(genres, values):
        if val < 0.1:  # 过滤掉极小值，避免太碎
            continue
        color = genre_colors.get(genre, default_color)
        # 绘制该类型在这个地区的条形
        rect = ax.barh(
            y=y_idx,
            width=val,
            left=left,
            color=color,
            height=0.6,
            label=genre if y_idx == 0 else ""  # 只在第一个地区加图例，避免重复
        )
        # 添加百分比标签（只显示>2%的）
        if val > 2:
            ax.text(
                left + val/2,
                y_idx,
                f'{val:.1f}%',
                ha='center', va='center',
                color='white', fontweight='bold', fontsize=8
            )
        left += val  # 堆叠到下一个类型

# 美化
# 设置y轴标签
ax.set_yticks(y_positions)
ax.set_yticklabels(region_labels, fontsize=12)
# 设置x轴
ax.set_xlabel('销量占比 (%)', fontsize=14)
ax.set_xlim(0, 100)
# 标题
ax.set_title('各地区游戏类型销量占比（每个地区独立降序排列）', fontsize=18, pad=20)
# 移除边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
# 图例（去重+放在右侧）
handles, labels = ax.get_legend_handles_labels()
unique_handles = []
unique_labels = []
for h, l in zip(handles, labels):
    if l not in unique_labels:
        unique_labels.append(l)
        unique_handles.append(h)
ax.legend(unique_handles, unique_labels, bbox_to_anchor=(1.05, 1), loc='upper left', title='游戏类型')

plt.tight_layout(rect=[0, 0, 0.9, 1])
plt.show()
```

