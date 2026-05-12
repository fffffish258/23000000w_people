from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.item import Item, db

# 定義 Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    顯示首頁物品列表。
    - 取得關鍵字 q 與分類 cat
    - 呼叫 Item.get_all_available() 進行自動過期隱藏與狀態過濾
    - 渲染 index.html
    """
    keyword = request.args.get('q', '').strip()
    category = request.args.get('cat', 'All')
    
    items = Item.get_all_available(keyword=keyword, category=category)
    return render_template('index.html', items=items, q=keyword, cat=category)

@main_bp.route('/items/new', methods=['GET', 'POST'])
def create_item():
    """
    發佈新物品。
    - GET: 渲染 create.html
    - POST: 接收表單、驗證、寫入 DB、重導向至 index
    """
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', 'Misc')
        description = request.form.get('description', '').strip()
        image_url = request.form.get('image_url', '').strip()
        expiry_date_str = request.form.get('expiry_date', '')

        # 基本驗證
        if not title:
            flash("物品名稱是必填的！", "danger")
            return render_template('create.html')

        expiry_date = None
        if category == 'Food':
            if not expiry_date_str:
                flash("食品類物品必須填寫有效日期！", "danger")
                return render_template('create.html')
            try:
                expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash("日期格式不正確，請使用 YYYY-MM-DD", "danger")
                return render_template('create.html')

        # 建立物品
        new_item = Item.create(
            title=title,
            category=category,
            description=description,
            image_url=image_url,
            expiry_date=expiry_date
        )

        if new_item:
            flash(f"「{title}」已成功發佈！", "success")
            return redirect(url_for('main.index'))
        else:
            flash("發佈失敗，請稍後再試。", "danger")
            return render_template('create.html')

    return render_template('create.html')

@main_bp.route('/items/<int:id>')
def item_detail(id):
    """
    查看特定物品詳情。
    - 根據 id 查詢物品
    - 渲染 detail.html
    """
    item = Item.get_by_id(id)
    if not item:
        flash("找不到該物品！", "warning")
        return redirect(url_for('main.index'))
    return render_template('detail.html', item=item)

@main_bp.route('/items/<int:id>/take', methods=['POST'])
def take_item(id):
    """
    將物品標記為已領取。
    - 根據 id 查詢物品
    - 呼叫 item.mark_as_taken()
    - 重導向至 index
    """
    item = Item.get_by_id(id)
    if item:
        if item.mark_as_taken():
            flash(f"已將「{item.title}」標記為已領取！", "info")
        else:
            flash("更新狀態失敗。", "danger")
    else:
        flash("找不到該物品。", "warning")
    return redirect(url_for('main.index'))

@main_bp.route('/items/<int:id>/delete', methods=['POST'])
def delete_item(id):
    """
    刪除物品。
    - 根據 id 刪除資料
    - 重導向至 index
    """
    item = Item.get_by_id(id)
    if item:
        title = item.title
        if item.delete():
            flash(f"已刪除「{title}」。", "secondary")
        else:
            flash("刪除失敗。", "danger")
    else:
        flash("找不到該物品。", "warning")
    return redirect(url_for('main.index'))
