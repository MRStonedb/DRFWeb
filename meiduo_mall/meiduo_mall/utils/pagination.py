"""
把分页作为单一模块独立出来
"""

from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    # 默认每页条数，前端不指明时，按次数
    page_size = 2
    # 前端访问指明每页数量的参数名
    page_size_query_param = 'page_size'
    # 限制前端指明每页数量的最大值，超过时按这个值返回
    max_page_size = 20