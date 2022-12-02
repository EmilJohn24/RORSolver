from sympy import symbols, Eq, solve, solveset, nsolve

i = symbols('i')


def V(val=1.0, form="None", n=0, g=0.0):
    single_val_expr = {
        "None": val + (i * 0),
        "F/P": val * (1 + i) ** n,
        "P/F": val * (1 + i) ** -n,
        "F/A": val * ((1 + i) ** n - 1) / i,
        "A/F": val * i / ((1 + i) ** n - 1),
        "P/A": val * (((1 + i) ** n) - 1) / (i * ((1 + i) ** n)),
        "A/P": val * (i * (1 + i) ** n) / (((1 + i) ** n) - 1),
        "A/G": val * ((1 / i) - (n / (((1 + i) ** n) - 1))),
        "P/G": val * ((1 / i) * (((1 + i) ** n - 1) / (i * (1 + i) ** n)) - (n / (1 + i) ** n)),
        "F/G": val * ((1 / i) * ((((1 + i) ** n - 1) / i) - n)),
        "F/C": val * (((1 + g) ** n) - ((1 + i) ** n)) / (g - i),
        "P/C": val * ((((1 + g) ** n) * ((1 + i) ** -n)) - 1) / (g - i),
    }
    return single_val_expr[form]


def _V(val=1.0, form="None", interest=0.0, n=0, g=0.0):
    return V(val, form, n, g).subs(i, interest)


def _F(form="None", interest=0.0, n=0):
    return _V(val=1, form=form, interest=interest, n=n)


def irr(revenues, expenditures):
    return nsolve(Eq(revenues, expenditures), 0.1)


def err(outflow, inflow, n=0, e=0.0):
    outflow_value = outflow.subs(i, e)
    inflow_value = inflow.subs(i, e)
    return nsolve(Eq(outflow_value * V(1, "F/P", n), inflow_value), 0.1)


def payback(receipts, expenses, investment, resell=0.0, resell_year=5, simple=True, interest=0.0):
    receipt_periodic = sum(receipts)
    expense_periodic = sum(expenses)
    investment = -abs(investment)
    cumulative_pw = [investment]
    cash_flow = [investment]
    while True:
        value = receipt_periodic - expense_periodic
        if resell_year == len(cash_flow):
            value += resell
        if not simple:
            value *= _F("P/F", interest=interest, n=len(cash_flow))
        investment += value

        cumulative_pw.append(investment)
        cash_flow.append(value)

        if investment >= 0:
            break
    return len(cumulative_pw) - 1, cash_flow, cumulative_pw


def main():
    sol = _V(13000) + _V(5720, "P/A", 0.1, 5)
    # sol = _V(_V(6000) + _V(7800, "P/A", 0.1, 5), "A/P", 0.1, 5)
    sol = _V(sol, "A/P", 0.1, 5)
    # IRR Sample:
    ans = irr(V(1_200, "P/A", 8) + V(10_000, "P/F", 8),
              V(20_000))
    print(f'IRR:{ans}')

    # ERR Sample:
    ans = err(V(180_000) + V(5_000, "P/A", 3),
              V(3_000) + V(15_000, "F/A", 7),
              n=10,
              e=0.2, )
    print(f'ERR:{ans}')

    # A/G Test:
    print(
        _V(-33_200, "A/P", 0.2, 5) - 2_165 - (1_100 + _V(500, "A/G", 0.2, 5))
    )

    print(
        _V(-47_600, "A/P", 0.2, 9) + _V(5_000, "A/F", 0.2, 9)
        - 1_720 - ((500 * _F("F/A", 0.2, 6) + 100 * _F("F/G", 0.2, 6)) *
                   _F("P/F", 0.2, 9) * _F("A/P", 0.2, 9))
    )
    print(_V(1_000, "F/C", 0.15, 6, g=0.12))
    print(_V(1_000, "P/C", 0.15, 6, g=0.12))

    # Q11
    print(
        err(V(15_000) + V(3_000, "P/A", 5),
            V(10_000, "F/A", 5) + V(15_000 * 0.15),
            e=0.15,
            n=5, )
    )

    # Q12
    years, cash_flow, cum_pws = payback(
        receipts=[2_700_000, ],
        expenses=[0, ],
        investment=13_500_000,
        simple=False,
        interest=0.15,
    )
    print(years)
    print(cash_flow)
    print(cum_pws)

    # Payback Example in PPT
    years, cash_flow, cum_pws = payback(
        receipts=[8_000, ],
        expenses=[0, ],
        investment=25_000,
        resell=5_000,
        resell_year=5,
        simple=False,
        interest=0.20,
    )
    print(years)
    print(cash_flow)
    print(cum_pws)


if __name__ == '__main__':
    main()
