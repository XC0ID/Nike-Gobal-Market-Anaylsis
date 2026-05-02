# Models

Place trained model artifacts here (`.pkl`, `.joblib`, `.json`).

## Planned Models

| Model | Goal | Features |
|---|---|---|
| `demand_forecast.pkl` | Predict restocking need | availability_level, size_count, category, country |
| `price_elasticity.pkl` | Estimate price sensitivity | price_usd, discount_pct, in_stock, sport_tags |
| `oos_classifier.pkl` | Classify OOS risk | size_count, available_size_count, category, gender |

## Training

```bash
# Example — train OOS classifier
python src/models/train_oos_classifier.py --country US --output models/oos_classifier.pkl
```
