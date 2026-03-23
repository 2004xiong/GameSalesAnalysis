"""
代码是在Jupyter Notebook上面按代码块跑的，此为整合代码
Jupyter Notebook 运行结果 https://gist.github.com/2004xiong/56abd95fc8aff62dba4b0b64251e6900
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
