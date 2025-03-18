from dosuby.src.adapter.crt.crt_adapter import CrtAdapter
from dosuby.infrastructure.libs.CrtSearch.crt_search import CrtSearch


# def test_crt_search_return_correct_data():
#     # crt_adapter = CrtAdapter()
#     crt_search = CrtSearch()
#     rs = crt_search.search(query='uca.ma')
#     data = []
#     i = 0
#     for r in rs:
#         cells = r.find_all("td")
#         # Check if there are at least 5 cells in the row
#         if len(cells) >= 5:
#             fifth_cell = cells[4]
#             data.append(fifth_cell.text)
    
#     assert data[1] == 'yyy.este.uca.ma'
#     assert data[4] == 'ecampus-cloud.uca.ma'
#     assert data[11] == 'rh-ensas.uca.ma'
    
