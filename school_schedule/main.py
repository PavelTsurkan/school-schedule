import gjango_setup
from main.models import *
from datetime import datetime
import time


# Додавання предмета
def add_subject():
    name = input("Введіть назву предмету: ")
    if not Subject.objects.filter(name=name).exists():
        subject = Subject(name=name)
        subject.save()
        print(f"Предмет '{name}' успішно доданий.")
        time.sleep(1.5)
    else:
        print(f"Предмет '{name}' вже існує.")
        time.sleep(1.5)


# Додавання учителя та пов'язання з його предметом
def add_teacher():
    name = input("Введіть ім'я вчителя: ")
    subject_name = input("Введіть назву предмету: ")
    try:
        subject = Subject.objects.get(name=subject_name)
        teacher, created = Teacher.objects.get_or_create(name=name, subject=subject)
        if created:
            print(f"Вчитель '{name}' успішно доданий.")
            time.sleep(1.5)
        else:
            print(f"Вчитель '{name}' вже існує.")
            time.sleep(1.5)

    except Subject.DoesNotExist:
        print(f"Предмет '{subject_name}' не існує.")
        time.sleep(1.5)


# Додавання класу
def add_class():
    name = input("Введіть назву класу: ")
    try:
        if not Class.objects.filter(name=name).exists():
            class_obj = Class(name=name)
            class_obj.save()
            print(f"Клас '{name}' успішно доданий.")
            time.sleep(1.5)
        else:
            print(f"Клас '{name}' вже існує.")
            time.sleep(1.5)

    except gjango_setup.django.core.exceptions.FieldError:
        print("Виникла помилка: поле 'year' не знайдено у моделі 'Class'.")
        time.sleep(1.5)


# Додавання учнів
def add_student():
    name = input("Введіть ім'я учня: ")
    class_name = input("Введіть назву класу: ")
    try:
        class_obj = Class.objects.get(name=class_name)
        student, created = Student.objects.get_or_create(name=name, class_name=class_obj)
        if created:
            print(f"Учень '{name}' успішно доданий.")
            time.sleep(1.5)
        else:
            print(f"Учень '{name}' вже існує.")
            time.sleep(1.5)
            
    except Class.DoesNotExist:
        print(f"Клас '{class_name}' не існує.")
        time.sleep(1.5)


# Додавання розкаладу
def add_schedule():
    day = input("Введіть день тижня: ")
    time_str = input("Введіть час початку у форматі HH:MM: ")
    subject_name = input("Введіть назву предмету: ")
    teacher_name = input("Введіть ім'я вчителя: ")
    class_name = input("Введіть назву класу: ")

    try:
        subject = Subject.objects.get(name=subject_name)
        teacher = Teacher.objects.get(name=teacher_name)
        class_obj = Class.objects.get(name=class_name)

        time = datetime.strptime(time_str, "%H:%M").time()

        schedule = Schedule(subject=subject, teacher=teacher, class_name=class_obj, day=day, time=time)
        schedule.save()
        print("Заняття успішно додано до розкладу.")
        time.sleep(1.5)

    except Subject.DoesNotExist:
        print(f"Предмет '{subject_name}' не існує.")
        time.sleep(1.5)

    except Teacher.DoesNotExist:
        print(f"Вчитель '{teacher_name}' не існує.")
        time.sleep(1.5)

    except Class.DoesNotExist:
        print(f"Клас '{class_name}' не існує.")
        time.sleep(1.5)

    except ValueError:
        print("Неправильний формат часу.")
        time.sleep(1.5)


# Додавання оцінок
def add_grade():
    student_name = input("Введіть ім'я учня: ")
    subject_name = input("Введіть назву предмету: ")
    grade_value = input("Введіть оцінку: ")

    try:
        student = Student.objects.get(name=student_name)
        subject = Subject.objects.get(name=subject_name)
        grade = float(grade_value)

        new_grade = Grade(student=student, subject=subject, grade=grade)
        new_grade.save()
        print("Оцінка успішно додана.")
        time.sleep(1.5)

    except Student.DoesNotExist:
        print(f"Учень '{student_name}' не існує.")
        time.sleep(1.5)

    except Subject.DoesNotExist:
        print(f"Предмет '{subject_name}' не існує.")
        time.sleep(1.5)

    except ValueError:
        print("Неправильний формат оцінки або дати.")
        time.sleep(1.5)


# Показ усіх учнів та їх класи
def show_students():
    students = Student.objects.all()
    if students:
        print("Список учнів:")
        for student in students:
            print(f"- {student.name} ({student.class_name})")
    else:
        print("Немає даних про учнів. Додайте учня за допомогою опції '4. Додати учня'.")
        time.sleep(1.5)


# Показ учителів та їх предметів
def show_teachers():
    teachers = Teacher.objects.all()
    if teachers:
        print("Список вчителів:")
        for teacher in teachers:
            print(f"- {teacher.name} ({teacher.subject})")
    else:
        print("Немає даних про вчителів. Додайте вчителя за допомогою опції '2. Додати вчителя'.")
        time.sleep(1.5)


# Показ оцінок учнів разом з ними
def show_grades():
    students = Student.objects.all()
    if students:
        print("Оцінки учнів:")
        for student in students:
            grades = Grade.objects.filter(student=student)
            if grades:
                print(f"- {student.name}:")
                for grade in grades:
                    print(f"  - {grade.subject}: {grade.grade}")
            else:
                print(f"- {student.name}: немає оцінок. Додайте оцінку за допомогою опції '6. Додати оцінку'.")
                time.sleep(1.5)
    else:
        print("Немає даних про учнів. Додайте учня за допомогою опції '4. Додати учня'.")
        time.sleep(1.5)


# Показ розкладу заннять
def show_schedule():
    days = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', 'П\'ятниця']
    print("Розклад дня:")
    has_schedule = False
    for day in days:
        schedule = Schedule.objects.filter(day=day)
        if schedule:
            has_schedule = True
            print(f"\n{day}:")
            for lesson in schedule:
                print(f"  - {lesson.time}: {lesson.subject} ({lesson.teacher}) в класі {lesson.class_name}")
    if not has_schedule:
        print("Немає розкладу для жодного дня. Додайте заняття в розклад за допомогою опції '5. Додати заняття в розклад'.")
        time.sleep(1.5)


# Головна функція
def main():
    while True:
        print("\nМеню:")

        print("\n1. Додати предмет")
        print("2. Додати вчителя")
        print("3. Додати клас")
        print("4. Додати учня")
        print("5. Додати заняття в розклад")
        print("6. Додати оцінку")

        print("\n7. Показати список учнів")
        print("8. Показати список вчителів")
        print("9. Показати оцінки учнів")
        print("10. Показати розклад дня")

        print("\n0. Вийти")

        choice = input("\nВиберіть опцію: ")

        # Вибір опції з додавання даних
        if choice == "1":
            add_subject()
        elif choice == "2":
            add_teacher()
        elif choice == "3":
            add_class()
        elif choice == "4":
            add_student()
        elif choice == "5":
            add_schedule()
        elif choice == "6":
            add_grade()

        # Вибір опції з отримання даних
        if choice == "7":
            show_students()
        elif choice == "8":
            show_teachers()
        elif choice == "9":
            show_grades()
        elif choice == "10":
            show_schedule()
        
        # Завершення роботи програми
        elif choice == "0":
            print("Дякую за користування! Завершення програми.")
            break
        else:
            print("Такої опції немає. Будь ласка, обреріть з існуючих.")
            time.sleep(1.5)


if __name__ == "__main__":
    main()

