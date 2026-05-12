from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.item import Item

# 定義 Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    顯示首頁物品列表。
    - 取得關鍵字 q 與分類 cat
    - 呼叫 Item.get_all_available() 並進行後續篩選
    - 渲染 index.html
    """
    return "Index Page"

@main_bp.route('/items/new', methods=['GET', 'POST'])
def create_item():
    """
    發佈新物品。
    - GET: 渲染 create.html
    - POST: 接收表單、驗證、寫入 DB、重導向至 index
    """
    if request.method == 'POST':
        return redirect(url_for('main.index'))
    return "Create Item Page"

@main_bp.route('/items/<int:id>')
def item_detail(id):
    """
    查看特定物品詳情。
    - 根據 id 查詢物品
    - 渲染 detail.html
    """
    return f"Item Detail Page: {id}"

@main_bp.route('/items/<int:id>/take', methods=['POST'])
def take_item(id):
    """
    將物品標記為已領取。
    - 根據 id 查詢物品
    - 呼叫 item.mark_as_taken()
    - 重導向至 index
    """
    return redirect(url_for('main.index'))

@main_bp.route('/items/<int:id>/delete', methods=['POST'])
def delete_item(id):
    """
    刪除物品。
    - 根據 id 刪除資料
    - 重導向至 index
    """
    return redirect(url_for('main.index'))
