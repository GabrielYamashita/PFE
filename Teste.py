
import locale

locale.setlocale(locale.LC_ALL, 'pt-BR.utf-8')


net_worth = 1796291.5729885271

x = locale.format_string("%.2f", net_worth, grouping=True, monetary=True)

print(f"Price {x}")