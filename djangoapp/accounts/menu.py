from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class MenuItem:
    def __init__(self, title, url=None, icon=None, permissions=None, children=None):
        self.title = title
        self.url = url
        self.icon = icon or "bi bi-circle"
        self.permissions = permissions or []
        self.children = children or []

    def has_permission(self, user):
        """Verifica se o usuário tem permissão para ver este item de menu"""
        if not self.permissions:
            return True
        return any(user.has_perm(perm) for perm in self.permissions)

    def get_visible_children(self, user):
        """Retorna apenas os filhos que o usuário tem permissão para ver"""
        return [child for child in self.children if child.has_permission(user)]

    def is_active(self, current_url):
        """Verifica se este item de menu está ativo"""
        if self.url and current_url.startswith(self.url):
            return True
        return any(child.is_active(current_url) for child in self.children)

def get_menu_items(user):
    """
    Retorna todos os itens de menu baseado nas permissões do usuário.
    OBSERVAÇÃO: Todas as URLs marcadas com '/temp/' são temporárias e devem ser substituídas
    pelas URLs reais quando os respectivos apps e views forem criados.
    """
    menu_items = [
        MenuItem(
            title=_("Principal"),
            children=[
                MenuItem(
                    title=_("Dashboard"),
                    url=reverse('dashboard'),  # URL já existente
                    icon="bi bi-speedometer2"
                ),
            ]
        ),
        MenuItem(
            title=_("Vendas"),
            permissions=['sales.view_sale', 'sales.view_customer'],
            children=[
                MenuItem(
                    title=_("Vendas"),
                    icon="bi bi-cart",
                    permissions=['sales.view_sale'],
                    children=[
                        MenuItem(
                            title=_("Lista de Vendas"),
                            url='/temp/sales/list/',  # TODO: Criar view de listagem de vendas
                            icon="bi bi-list-ul",
                            permissions=['sales.view_sale']
                        ),
                        MenuItem(
                            title=_("Nova Venda"),
                            url='/temp/sales/new/',  # TODO: Criar view de criação de venda
                            icon="bi bi-plus-circle",
                            permissions=['sales.add_sale']
                        ),
                        MenuItem(
                            title=_("Relatórios de Vendas"),
                            url='/temp/sales/reports/',  # TODO: Criar view de relatórios de vendas
                            icon="bi bi-graph-up",
                            permissions=['sales.view_sale']
                        ),
                    ]
                ),
                MenuItem(
                    title=_("Clientes"),
                    url='/temp/customers/',  # TODO: Criar app/view de clientes
                    icon="bi bi-people",
                    permissions=['sales.view_customer']
                ),
            ]
        ),
        MenuItem(
            title=_("Estoque"),
            permissions=['inventory.view_product'],
            children=[
                MenuItem(
                    title=_("Produtos"),
                    icon="bi bi-box-seam",
                    permissions=['inventory.view_product'],
                    children=[
                        MenuItem(
                            title=_("Lista de Produtos"),
                            url='/temp/inventory/products/',  # TODO: Criar view de listagem de produtos
                            icon="bi bi-list-ul",
                            permissions=['inventory.view_product']
                        ),
                        MenuItem(
                            title=_("Novo Produto"),
                            url='/temp/inventory/products/new/',  # TODO: Criar view de novo produto
                            icon="bi bi-plus-circle",
                            permissions=['inventory.add_product']
                        ),
                        MenuItem(
                            title=_("Categorias"),
                            url='/temp/inventory/categories/',  # TODO: Criar view de categorias
                            icon="bi bi-tags",
                            permissions=['inventory.view_category']
                        ),
                        MenuItem(
                            title=_("Controle de Estoque"),
                            url='/temp/inventory/stock/',  # TODO: Criar view de controle de estoque
                            icon="bi bi-boxes",
                            permissions=['inventory.view_stock']
                        ),
                    ]
                ),
            ]
        ),
        MenuItem(
            title=_("Financeiro"),
            permissions=['financial.view_transaction'],
            children=[
                MenuItem(
                    title=_("Visão Geral"),
                    url='/temp/financial/overview/',  # TODO: Criar view de visão geral financeira
                    icon="bi bi-cash-coin",
                    permissions=['financial.view_transaction']
                ),
                MenuItem(
                    title=_("Contas a Receber"),
                    url='/temp/financial/receivables/',  # TODO: Criar view de contas a receber
                    icon="bi bi-arrow-down-circle",
                    permissions=['financial.view_receivable']
                ),
                MenuItem(
                    title=_("Contas a Pagar"),
                    url='/temp/financial/payables/',  # TODO: Criar view de contas a pagar
                    icon="bi bi-arrow-up-circle",
                    permissions=['financial.view_payable']
                ),
            ]
        ),
        MenuItem(
            title=_("Relatórios"),
            permissions=['reports.view_report'],
            children=[
                MenuItem(
                    title=_("Relatórios Gerais"),
                    url='/temp/reports/',  # TODO: Criar app/view de relatórios
                    icon="bi bi-file-earmark-bar-graph",
                    permissions=['reports.view_report']
                ),
            ]
        ),
    ]

    # Adiciona menu de configurações para staff
    if user.is_staff:
        menu_items.append(
            MenuItem(
                title=_("Sistema"),
                children=[
                    MenuItem(
                        title=_("Configurações"),
                        url="#",  # Adicione a URL correta
                        icon="bi bi-gear",
                    ),
                ]
            )
        )

    # Adiciona menu de administração para superusuários
    if user.is_superuser:
        menu_items[-1].children.append(
            MenuItem(
                title=_("Administração"),
                url=reverse('admin:index'),
                icon="bi bi-shield-lock",
            )
        )

    return menu_items