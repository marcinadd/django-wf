from wyniki.models import Result


def get_best_result_for_sport(sport):
    best_results_set = Result.objects.filter(sport=sport).order_by("-value" if sport.more_better else "value")
    return best_results_set[0] if len(best_results_set) > 0 else None


def create_results_list_for_student_and_sport(sport, student):
    results = []
    for group in Result.GROUP_CHOICES:
        try:
            result = Result.objects.get(student=student, group=group[0], sport=sport)
            results.append(result)
        except Result.DoesNotExist:
            results.append(None)
    return results
