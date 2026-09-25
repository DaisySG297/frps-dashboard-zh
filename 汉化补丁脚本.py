# -*- coding: utf-8 -*-
# 完整汉化补丁：按顺序精确替换（带键名的替换优先，防止误伤）
import sys

JS = r'C:\DaisySG Server\Frp\dashboard-static\index-BTokoqTQ.js'
js = open(JS, encoding='utf-8').read()
orig = js

# (旧, 新, 预期最少出现次数)
repls = [
    # --- 残留的业务界面文案 ---
    ('?"已启用":"Disabled"', '?"已启用":"已禁用"', 2),
    ('?"Connected":"Disconnected"', '?"已连接":"已断开"', 1),
    ('"Protocol"', '"协议"', 1),
    ('"Loading..."', '"加载中..."', 1),
    ('"Search proxies..."', '"搜索代理..."', 2),
    ('No proxies match "', '没有匹配的代理 "', 2),
    ('"Failed to fetch proxies: "', '"获取代理列表失败："', 1),
    ('"Failed to fetch clients: "', '"获取客户端列表失败："', 1),
    ('"Failed to fetch client: "', '"获取客户端详情失败："', 1),
    ('"Failed to fetch proxy: "', '"获取代理详情失败："', 1),
    ('"Failed to clear offline proxies: "', '"清理离线代理失败："', 1),
    ('"Get traffic info failed! "', '"获取流量信息失败！"'),
    ('"Invalid API v2 response"', '"API v2 响应无效"', 1),
    # 自定义相对时间函数
    ('" years ago"', '" 年前"', 1),
    ('" months ago"', '" 个月前"', 1),
    ('" days ago"', '" 天前"', 1),
    ('" hours ago"', '" 小时前"', 1),
    ('" minutes ago"', '" 分钟前"', 1),
    ('" seconds ago"', '" 秒前"', 1),
    # --- 确认对话框组件 ---
    ('confirmText:{default:"Confirm"}', 'confirmText:{default:"确认"}', 1),
    ('cancelText:{default:"Cancel"}', 'cancelText:{default:"取消"}', 1),
    # --- Element Plus 英文 locale（界面可见部分）---
    ('table:{emptyText:"No Data",confirmFilter:"Confirm",resetFilter:"Reset",clearFilter:"所有",sumText:"Sum"',
     'table:{emptyText:"暂无数据",confirmFilter:"筛选",resetFilter:"重置",clearFilter:"所有",sumText:"合计"', 1),
    ('pageHeader:{title:"Back"},popconfirm:{confirmButtonText:"Yes",cancelButtonText:"No"}',
     'pageHeader:{title:"返回"},popconfirm:{confirmButtonText:"是",cancelButtonText:"否"}', 1),
    ('pagination:{goto:"Go to",pagesize:"/page",total:"Total {total}",pageClassifier:"",page:"Page",prev:"Go to previous page",next:"Go to next page",currentPage:"page {pager}",prevPages:"Previous {pager} pages",nextPages:"Next {pager} pages"',
     'pagination:{goto:"前往",pagesize:"/页",total:"共 {total} 条",pageClassifier:"",page:"第",prev:"前往上一页",next:"前往下一页",currentPage:"第 {pager} 页",prevPages:"向前 {pager} 页",nextPages:"向后 {pager} 页"', 1),
    ('select:{loading:"Loading",noMatch:"No matching data",noData:"No data",placeholder:"Select"}',
     'select:{loading:"加载中",noMatch:"无匹配数据",noData:"暂无数据",placeholder:"请选择"}', 1),
    ('mention:{loading:"Loading"}', 'mention:{loading:"加载中"}', 1),
    ('noMatch:"No matching data",loading:"Loading",placeholder:"Select",noData:"No data"',
     'noMatch:"无匹配数据",loading:"加载中",placeholder:"请选择",noData:"暂无数据"', 1),
    ('tree:{emptyText:"No Data"}', 'tree:{emptyText:"暂无数据"}', 1),
    ('transfer:{noMatch:"No matching data",noData:"No data",titles:["List 1","List 2"],filterPlaceholder:"Enter keyword"',
     'transfer:{noMatch:"无匹配数据",noData:"暂无数据",titles:["列表 1","列表 2"],filterPlaceholder:"输入关键词"', 1),
    # datepicker / messagebox 按钮类
    ('cancel:"Cancel",clear:"清除",confirm:"OK"', 'cancel:"取消",clear:"清除",confirm:"确定"', 1),
    ('messagebox:{title:"Message",confirm:"OK",cancel:"Cancel",error:"Illegal input",close:"Close this dialog"}',
     'messagebox:{title:"提示",confirm:"确定",cancel:"取消",error:"输入不合法",close:"关闭此对话框"}', 1),
]

total = 0
missed = []
for old, new, *exp in repls:
    c = js.count(old)
    if c == 0:
        missed.append(old)
        continue
    js = js.replace(old, new)
    total += c
    if exp and c < exp[0]:
        print(f'警告: {old[:40]!r} 出现 {c} 次, 预期 {exp[0]}')

open(JS, 'w', encoding='utf-8').write(js)
print(f'替换完成: {total} 处 | 大小 {len(orig)} -> {len(js)}')
if missed:
    print('未找到(可能已翻译):')
    for m in missed:
        print('  -', m[:60])
