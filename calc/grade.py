def calc_average():
    total_score = 0
    num_tests = 8
    print("Enter 8 test scores (each out of 100):")
    
    for i in range(num_tests):
        while True:
            try:
                score = float(input(f"Enter score for test {i+1}: "))
                if 0 <= score <= 100:
                    total_score += score
                    break
                else:
                    print("Score must be between 0 and 100. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

    average_score = total_score / num_tests
    return average_score

def determine_grade(average_score):
    if 90 <= average_score <= 100:
        return 'A'
    elif 80 <= average_score < 90:
        return 'B'
    elif 70 <= average_score < 80:
        return 'C'
    elif 60 <= average_score < 70:
        return 'D'
    else:
        return 'F'

def main():
    average_score = calc_average()
    grade = determine_grade(average_score)
    
    print(f"\nThe average test score is: {average_score:.2f}")
    print(f"The corresponding letter grade is: {grade}")

if __name__ == "__main__":
    main()
