from math import ceil

def paginationInfo(total, pagina, porPagina):

    itemsPorPagina = porPagina if total >= porPagina else total

    totalPaginas = ceil(total / itemsPorPagina) if itemsPorPagina > 0 else 0

    paginaPrevia = pagina - 1 if pagina > 1 and pagina <= totalPaginas else None

    paginaSiguiente = pagina + 1 if totalPaginas > 1 and pagina < totalPaginas else None

    return{
        'porPagina': itemsPorPagina,
        'total': total,
        'pagina': pagina,
        'paginaPrevia': paginaPrevia,
        'paginaSiguiente': paginaSiguiente,
        'totalPaginas': totalPaginas
    }


