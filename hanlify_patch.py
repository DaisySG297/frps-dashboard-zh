# -*- coding: utf-8 -*-
"""
frps 官方面板汉化补丁脚本（frp v0.71.0）

用法：
    python hanlify_patch.py <面板目录>

其中 <面板目录> 是已从 http://<frps>:7500/static/ 下载好的
index.html 及其引用的 JS/CSS 所在目录。

原理：对官方面板 JS 中的字符串字面量做精确替换（含 frp_zh 项目
映射无法覆盖的状态徽标、按钮、分页、弹窗、相对时间等），不动任何
逻辑代码。替换后建议用 node --check 校验一次 JS 语法。
"""
import os
import sys

# 第一步：从 Firfr/frp_zh 项目的汉化映射 JSON 应用翻译（见其仓库说明）
# 第二步：应用本脚本的人工补充规则（如下）

REPLACEMENTS = [
    # --- 状态徽标 / 配置值 ---
    ('?"已启用":"Disabled"', '?"已启用":"已禁用"'),
    ('?"Connected":"Disconnected"', '?"已连接":"已断开"'),
    ('"Protocol"', '"协议"'),
    # API 返回的 status 原始值渲染映射（class 保留原值维持配色）
    (',J(e.proxy.status),3)', ',J("online"===e.proxy.status?"在线":"离线"),3)'),
    (',J(r.value.status),3)', ',J("online"===r.value.status?"在线":"离线"),3)'),
    # --- 按钮 / 侧边栏 / 标签 ---
    ('" Overview "', '" 总览 "'),
    ('" Clients "', '" 客户端 "'),
    ('" Proxies "', '" 代理 "'),
    ('" Refresh "', '" 刷新 "'),
    ('" Clear Offline "', '" 清理离线 "'),
    ('"Connections:"', '"连接数:"'),
    ('"Client:"', '"客户端:"'),
    ('"Port:"', '"端口:"'),
    ('" Traffic In"', '" 流入"'),
    ('" Traffic Out"', '" 流出"'),
    ('" Last Started "', '" 最近启动 "'),
    ('" Last Closed "', '" 最近关闭 "'),
    ('`In: ${', '`流入: ${'),
    ('`Out: ${', '`流出: ${'),
    # --- 加载 / 搜索 / 空状态 ---
    ('" No active proxies "', '" 暂无在线代理 "'),
    ('"Server"', '"服务端"'),
    ('"Loading..."', '"加载中..."'),
    ('"Search proxies..."', '"搜索代理..."'),
    ('placeholder:"Search clients..."', 'placeholder:"搜索客户端..."'),
    ('No proxies match "', '没有匹配的代理 "'),
    # --- 错误提示 ---
    ('"Failed to fetch proxies: "', '"获取代理列表失败："'),
    ('"Failed to fetch clients: "', '"获取客户端列表失败："'),
    ('"Failed to fetch client: "', '"获取客户端详情失败："'),
    ('"Failed to fetch proxy: "', '"获取代理详情失败："'),
    ('"Failed to clear offline proxies: "', '"清理离线代理失败："'),
    ('"Get traffic info failed! "', '"获取流量信息失败！"'),
    ('"Invalid API v2 response"', '"API v2 响应无效"'),
    ('message:"Are you sure you want to clear all offline proxies?"',
     'message:"确定要清除所有离线代理吗？"'),
    # --- 相对时间 ---
    ('" years ago"', '" 年前"'),
    ('" months ago"', '" 个月前"'),
    ('" days ago"', '" 天前"'),
    ('" hours ago"', '" 小时前"'),
    ('" minutes ago"', '" 分钟前"'),
    ('" seconds ago"', '" 秒前"'),
    # --- 确认对话框组件默认文案 ---
    ('confirmText:{default:"Confirm"}', 'confirmText:{default:"确认"}'),
    ('cancelText:{default:"Cancel"}', 'cancelText:{default:"取消"}'),
    # --- Element Plus 英文 locale（界面可见部分）---
    ('table:{emptyText:"No Data",confirmFilter:"Confirm",resetFilter:"Reset",clearFilter:"所有",sumText:"Sum"',
     'table:{emptyText:"暂无数据",confirmFilter:"筛选",resetFilter:"重置",clearFilter:"所有",sumText:"合计"'),
    ('pageHeader:{title:"Back"},popconfirm:{confirmButtonText:"Yes",cancelButtonText:"No"}',
     'pageHeader:{title:"返回"},popconfirm:{confirmButtonText:"是",cancelButtonText:"否"}'),
    ('pagination:{goto:"Go to",pagesize:"/page",total:"Total {total}",pageClassifier:"",page:"Page",prev:"Go to previous page",next:"Go to next page",currentPage:"page {pager}",prevPages:"Previous {pager} pages",nextPages:"Next {pager} pages"',
     'pagination:{goto:"前往",pagesize:"/页",total:"共 {total} 条",pageClassifier:"",page:"第",prev:"前往上一页",next:"前往下一页",currentPage:"第 {pager} 页",prevPages:"向前 {pager} 页",nextPages:"向后 {pager} 页"'),
    ('select:{loading:"Loading",noMatch:"No matching data",noData:"No data",placeholder:"Select"}',
     'select:{loading:"加载中",noMatch:"无匹配数据",noData:"暂无数据",placeholder:"请选择"}'),
    ('mention:{loading:"Loading"}', 'mention:{loading:"加载中"}'),
    ('noMatch:"No matching data",loading:"Loading",placeholder:"Select",noData:"No data"',
     'noMatch:"无匹配数据",loading:"加载中",placeholder:"请选择",noData:"暂无数据"'),
    ('tree:{emptyText:"No Data"}', 'tree:{emptyText:"暂无数据"}'),
    ('transfer:{noMatch:"No matching data",noData:"No data",titles:["List 1","List 2"],filterPlaceholder:"Enter keyword"',
     'transfer:{noMatch:"无匹配数据",noData:"暂无数据",titles:["列表 1","列表 2"],filterPlaceholder:"输入关键词"'),
    ('cancel:"Cancel",clear:"清除",confirm:"OK"', 'cancel:"取消",clear:"清除",confirm:"确定"'),
    ('messagebox:{title:"Message",confirm:"OK",cancel:"Cancel",error:"Illegal input",close:"Close this dialog"}',
     'messagebox:{title:"提示",confirm:"确定",cancel:"取消",error:"输入不合法",close:"关闭此对话框"}'),
]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    d = sys.argv[1]
    js_files = [os.path.join(d, f) for f in os.listdir(d) if f.endswith('.js')]
    if not js_files:
        print('目录里没有找到 JS 文件:', d)
        sys.exit(1)
    for p in js_files:
        js = open(p, encoding='utf-8').read()
        total = 0
        for old, new in REPLACEMENTS:
            c = js.count(old)
            js = js.replace(old, new)
            total += c
        open(p, 'w', encoding='utf-8').write(js)
        print('%s: 替换 %d 处' % (os.path.basename(p), total))
    print('完成。请刷新浏览器（Ctrl+F5）查看效果。')


if __name__ == '__main__':
    main()
