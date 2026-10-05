def calculate_taxable_income(
    gross_income,
    deductions
):

    if gross_income < 0:
        gross_income = 0

    if deductions < 0:
        deductions = 0

    taxable_income = gross_income - deductions

    if taxable_income < 0:
        taxable_income = 0

    return taxable_income