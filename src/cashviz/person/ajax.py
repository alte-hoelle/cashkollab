from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from cashviz.models.person import Person
from config import HELL_CONFIG


def person_fee_details(request: HttpRequest, person_id: int = 1) -> HttpResponse:
    persons = Person.member_and_supporter.all()
    all_payed_fees = sum(dx.payed_fees() for dx in persons)
    all_payed_support = sum(dx.payed_support() for dx in persons)
    all_support_open = sum(dx.support_open() for dx in persons)
    all_member_fees_open = sum(dx.member_fees_open() for dx in persons)

    if Person.objects.filter(id=person_id).exists():  # pylint: disable=no-member
        person = Person.objects.filter(id=person_id)[0]  # pylint: disable=no-member

        support_due = person.support_due()
        support_payed = person.payed_support()
        support_open = person.support_open()
        member_fees_due = person.member_fees_due()
        member_fees_payed = person.payed_fees()
        member_fees_open = person.member_fees_open()
        # print(f"{support_payed=} {support_due=} {support_payed - support_due}")
        # print(f"{member_fees_payed=} {member_fees_due=} {member_fees_payed - member_fees_due}")

        return render(
            request,
            "person/person_fee_details_ajax.html",
            {
                "support_amount": person.support_amount,
                "name": "anon" if HELL_CONFIG.anon_names else person.name,
                "member_fees_payed": member_fees_payed,
                "member_fees_due": member_fees_due,
                "member_fees_open": -member_fees_open,
                "all_member_fees_open": -all_member_fees_open,
                "all_payed_fees": all_payed_fees,
                "support_payed": support_payed,
                "support_due": support_due,
                "support_open": -support_open,
                "all_support_open": -all_support_open,
                "all_payed_support": all_payed_support,
                "member": person.is_member,
                "support": person.is_supporter,
                "fee_and_support_payments": person.fee_and_support_payments(),
                "fee_and_support_changes": person.fee_and_support_changes(),
                "fee_and_support_table": person.support_and_fee_table(),
            },
        )
    return render(
        request,
        "person/person_fee_details_ajax.html",
        {
            "support_amount": 0.0,
            "name": "",
            "member_fees_payed": 0.0,
            "member_fees_due": 0.0,
            "member_fees_open": 0.0,
            "all_member_fees_open": all_member_fees_open,
            "support_payed": 0.0,
            "support_due": 0.0,
            "support_open": 0.0,
            "all_support_open": all_support_open,
            "member": False,
            "support": False,
            "fee_and_support_payments": False,
            "all_payed_fees": all_payed_fees,
            "all_payed_support": all_payed_support,
        },
    )
