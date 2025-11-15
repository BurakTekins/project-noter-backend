from django.core.management.base import BaseCommand
from outcomes.models import ProgramLearningOutcome


class Command(BaseCommand):
    help = 'Populates the database with the 11 Program Learning Outcomes'

    def handle(self, *args, **options):
        plos_data = [
            {
                'number': 1,
                'short_name': 'Mathematics & Engineering Knowledge',
                'description': 'Gain adequate knowledge in mathematics, science and related engineering discipline subjects; ability to use theoretical and applied knowledge in these fields in complex engineering problems.',
                'category': 'KNOWLEDGE'
            },
            {
                'number': 2,
                'short_name': 'Problem Analysis & Solution',
                'description': 'Gain ability to identify, formulate and solve complex engineering problems; gain ability to choose and apply appropriate analysis and modeling methods for this purpose.',
                'category': 'SKILLS'
            },
            {
                'number': 3,
                'short_name': 'Design & Development',
                'description': 'Gain ability to design a complex system, process, device or product to meet certain requirements under realistic constraints and Conditions; ability to apply modern design methods for this purpose.',
                'category': 'SKILLS'
            },
            {
                'number': 4,
                'short_name': 'Modern Tools & IT',
                'description': 'Analyze and create solutions to complex problems encountered in engineering applications of modern techniques and tools for development, have skills, gain the ability to use information technology effectively.',
                'category': 'SKILLS'
            },
            {
                'number': 5,
                'short_name': 'Research & Experimentation',
                'description': 'Gain ability to design experiments, conduct experiments, collect data, analyze and interpret results for the study of complex engineering problems or discipline-specific research topics.',
                'category': 'SKILLS'
            },
            {
                'number': 6,
                'short_name': 'Teamwork & Individual Work',
                'description': 'Gain ability to work effectively in interdisciplinary and multidisciplinary teams; work individually.',
                'category': 'COMPETENCE'
            },
            {
                'number': 7,
                'short_name': 'Communication Skills',
                'description': 'Gain ability to communicate effectively in Turkish oral and written; knowledge of at least one foreign language; ability to write effective reports and understand written report, design and production reports, make effective presentations, give and receive clear and understandable instructions.',
                'category': 'COMPETENCE'
            },
            {
                'number': 8,
                'short_name': 'Lifelong Learning',
                'description': 'Gain awareness of of the need for lifelong learning; the ability to access information, monitor developments in science and technology, and constantly renew oneself.',
                'category': 'COMPETENCE'
            },
            {
                'number': 9,
                'short_name': 'Ethics & Professional Responsibility',
                'description': 'Act in accordance with ethical principles, awareness of professional and ethical responsibility; gain knowledge of standards used in engineering applications',
                'category': 'COMPETENCE'
            },
            {
                'number': 10,
                'short_name': 'Project Management & Entrepreneurship',
                'description': 'Gain knowledge of business practices such as Project Management, risk Management and change management; gain awareness about entrepreneurship, innovation; have information about sustainable development.',
                'category': 'COMPETENCE'
            },
            {
                'number': 11,
                'short_name': 'Social Impact & Legal Awareness',
                'description': 'Gain knowledge of the effects of engineering practices on health, environment and safety in Universal and social dimensions and the problems reflected in the field of engineering of the era; gain awareness of the legal consequences of engineering solutions.',
                'category': 'COMPETENCE'
            },
        ]

        created_count = 0
        updated_count = 0

        for plo_data in plos_data:
            plo, created = ProgramLearningOutcome.objects.update_or_create(
                number=plo_data['number'],
                defaults={
                    'short_name': plo_data['short_name'],
                    'description': plo_data['description'],
                    'category': plo_data['category'],
                    'is_active': True
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created PLO-{plo.number}: {plo.short_name}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated PLO-{plo.number}: {plo.short_name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully processed {len(plos_data)} PLOs '
                f'({created_count} created, {updated_count} updated)'
            )
        )
