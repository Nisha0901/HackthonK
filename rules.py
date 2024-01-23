class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3
    WHITE = 4

def total_revenue(data: dict, financial_index):
    financial_entry = data.get("financials")[financial_index]
    pnl_section = financial_entry.get("lineItems", {}).get("pnl", {})
    net_revenue = pnl_section.get("netRevenue", 0.0)
    return net_revenue

def total_borrowing(data: dict, financial_index):
    financial_entry = data.get("financials")[financial_index]
    bs_section = financial_entry.get("balanceSheet", {})
    long_term_borrowings = bs_section.get("longTermBorrowings", 0.0)
    short_term_borrowings = bs_section.get("shortTermBorrowings", 0.0)
    
    total_borrowings = long_term_borrowings + short_term_borrowings
    return total_borrowings

def iscr(data: dict, financial_index):
    financial_entry = data.get("financials")[financial_index]
    pnl_section = financial_entry.get("lineItems", {}).get("pnl", {})
    interest_expenses = pnl_section.get("interestExpenses", 0.0)
    profit_before_interest_tax = pnl_section.get("profitBeforeInterestAndTax", 0.0)
    depreciation = pnl_section.get("depreciation", 0.0)

    # Avoid division by zero
    iscr_value = (profit_before_interest_tax + depreciation + 1) / (interest_expenses + 1)
    return iscr_value

def iscr_flag(data: dict, financial_index):
    iscr_value = iscr(data, financial_index)
    return FLAGS.GREEN if iscr_value >= 2 else FLAGS.RED

def total_revenue_5cr_flag(data: dict, financial_index):
    total_revenue_value = total_revenue(data, financial_index)
    return FLAGS.GREEN if total_revenue_value >= 50000000 else FLAGS.RED

def borrowing_to_revenue_flag(data: dict, financial_index):
    """
    Determine the flag color based on the ratio of total borrowings to total revenue.

    This function calculates the ratio of total borrowings to total revenue by calling the total_borrowing
    function and then assigns a flag color based on the calculated ratio. If the ratio is less than or equal
    to 0.25, it assigns a GREEN flag, otherwise, it assigns an AMBER flag.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ratio calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.AMBER: The flag color based on the borrowing to revenue ratio.
    """
    total_borrowings = total_borrowing(data, financial_index)
    total_revenue_value = total_revenue(data, financial_index)

    # Check if total_revenue_value is zero to avoid division by zero
    if total_revenue_value == 0:
        return FLAGS.WHITE  # You can choose an appropriate flag for this case

    borrowing_to_revenue_ratio = total_borrowings / total_revenue_value

    # Assign flag based on the calculated ratio
    return FLAGS.GREEN if borrowing_to_revenue_ratio <= 0.25 else FLAGS.AMBER

def latest_financial_index(data: dict):
    """
    Determine the index of the latest financial entry in the data.

    This function iterates over the "financials" list in the given data dictionary.
    It returns the index of the latest financial entry based on the order in the list.
    If no financial entry is found, it returns 0.

    Parameters:
    - data (dict): A dictionary containing a list of financial entries under the "financials" key.

    Returns:
    - int: The index of the latest financial entry or 0 if not found.
    """
    financials = data.get("financials", [])
    if financials:
        return len(financials) - 1  # Return the index of the last financial entry
    return 0