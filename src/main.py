import pandas as pd
from load_data import load_csv
from clean_data import clean_sensor_data
from evaluate import WaterQualityEvaluator

def main():

    input_path = 'data/sensor_data.csv'
    output_path= 'data/results.csv'

    #Load data
    df = load_csv(input_path)

    #Clean data
    clean_df = clean_sensor_data(df)

    #Evaluate data
    evaluator = WaterQualityEvaluator()
    eval_df = evaluator.evaluate_all(clean_df)

    # Attach the results to the cleaned DataFrame
    evaluated_df = clean_df.copy()
    evaluated_df['is_safe'] = eval_df['is_safe']
    evaluated_df['reason'] = eval_df['reason']

    # Format output
    def format_eval(row: pd.Series) -> str:
        sensor = row.get('sensor_id')
        if row['is_safe']:
            return f"{sensor} is Safe"
        else:
            return f"{sensor} is Unsafe ({row['reason']})"

    evaluated_df['result'] = evaluated_df.apply(format_eval, axis=1)
    

    # Print results
    for line in evaluated_df['result'].tolist():
        print(line)

    # Save results
    evaluated_df['result'].to_csv(output_path, index=False)
    print(f"Results saved to {output_path}")


if __name__ == '__main__':
    main()

