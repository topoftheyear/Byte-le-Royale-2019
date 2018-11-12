# Trading

Trading is the legal way to make money. By buying and selling resources for profit, you will make a name for yourself and be a master of your trade.

## How to Trade

Trading is accomplished by entering the range of a station and using the `buy material` or `sell material` action.

## Buying

When you buy items, you specify the item you wish to purchase in the first parameter, and the amount in the second one.
Then, the following conditions are checked:
* buying more than available - will buy available amount
* buying more than you can afford - will buy as much as you can afford
* if 2 or more players both try a combined total more than store has in stock,
  each player will get (total amount / `n`) rounded up, where `n` is the number of players buying.


## Selling

When you sell items, you specify the item you wish to sell in the first parameter, and the amount in the second one.
Then, the following conditions are checked:
* selling more than available - will sell available amount
* selling more than you can afford - will sell as much as you can afford
* if 2 or more players both try a combined total more than store has in stock,
  each player will get (total amount / `n`) rounded up, where `n` is the number of players selling.


## Related Items

[Mining](asteroid_fields_and_mining.md)