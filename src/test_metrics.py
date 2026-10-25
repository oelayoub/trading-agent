import pytest
import pandas as pd
from src.metrics import calculate_metrics

#test mix results  
mix= pd.DataFrame({
    "Signal" : ["Strong Buy", "Buy", "Wait", "Buy"],
    "result" : ["win", "loss", None, "flat"],
    "week_to_result" : [4,9,None,3],
    "profit_loss" : [0.004,-0.02,None,0]
})

all_wins = pd.DataFrame({
    "Signal" : ["Strong Buy", "Buy", "Buy", "Buy"],
    "result" : ["win", "win", "win", "win"],
    "week_to_result" : [5,12,9,3],
    "profit_loss" : [0.01,0.03,0.02,0.05]
})

all_losses = pd.DataFrame({
    "Signal" : ["Strong Buy", "Buy", "Buy", "Buy"],
    "result" : ["loss", "loss", "loss", "loss"],
    "week_to_result" : [2,4,9,11],
    "profit_loss" : [-0.05,-0.02,-0.07,-0.1]
})

@pytest.mark.parametrize( # one test function and several inputs 

    "df, expected_result",
    [
        (mix, 3),
        (all_wins, 4),
        (all_losses, 4)
    ]

)

def test_calculate_metrics_trades(df, expected_result):
    assert calculate_metrics(df).get("Number of trades") == expected_result


@pytest.mark.parametrize( # Profit factor

    "df, expected_result",
    [
        (mix, 0.2),
        (all_wins, None),
        (all_losses, 0)
    ]

)

def test_calculate_profit_factor(df, expected_result):
    assert calculate_metrics(df).get("Profit Factor") == expected_result


@pytest.mark.parametrize( # Average week wins

    "df, expected_result",
    [
        (mix, 4),
        (all_wins, 7.25),
        (all_losses, 0)
    ]

)

def test_calculate_week_result(df, expected_result):
    assert calculate_metrics(df).get("Average week for wins") == expected_result

@pytest.mark.parametrize( # average week losses

    "df, expected_result",
    [
        (mix, 9),
        (all_wins, 0)

    ]

)

def test_calculate_week_losses(df, expected_result):
    assert calculate_metrics(df).get("Average week for losses") == expected_result


@pytest.mark.parametrize( # ratio wins  

    "df, expected_result",
    [
        (mix, 0.5),
        (all_wins, 1),
        (all_losses, 0)
    ]

)

def test_calculate_ratio_wins(df, expected_result):
    assert calculate_metrics(df).get("Wins ratio") == expected_result


