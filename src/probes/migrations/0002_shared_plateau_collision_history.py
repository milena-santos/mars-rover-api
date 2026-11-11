import uuid

import django.db.models.deletion
from django.db import migrations, models


def forwards_link_probes_to_plateaus(apps, schema_editor) -> None:
    PlateauRecord = apps.get_model("probes", "PlateauRecord")
    ProbeRecord = apps.get_model("probes", "ProbeRecord")

    plateau_by_size: dict[tuple[int, int], object] = {}
    for probe in ProbeRecord.objects.all():
        size = (probe.plateau_max_x, probe.plateau_max_y)
        plateau = plateau_by_size.get(size)
        if plateau is None:
            plateau = PlateauRecord.objects.create(
                id=uuid.uuid4(),
                max_x=probe.plateau_max_x,
                max_y=probe.plateau_max_y,
            )
            plateau_by_size[size] = plateau
        probe.plateau = plateau
        probe.save(update_fields=["plateau"])


class Migration(migrations.Migration):
    dependencies = [
        ("probes", "0001_create_probe_record"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlateauRecord",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("max_x", models.PositiveIntegerField()),
                ("max_y", models.PositiveIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ("created_at",),
            },
        ),
        migrations.CreateModel(
            name="ProbeCommandLogRecord",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("commands", models.TextField()),
                ("x", models.IntegerField()),
                ("y", models.IntegerField()),
                (
                    "direction",
                    models.CharField(
                        choices=[
                            ("NORTH", "NORTH"),
                            ("EAST", "EAST"),
                            ("SOUTH", "SOUTH"),
                            ("WEST", "WEST"),
                        ],
                        max_length=5,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "probe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="command_logs",
                        to="probes.proberecord",
                    ),
                ),
            ],
            options={
                "ordering": ("created_at",),
            },
        ),
        migrations.AddField(
            model_name="proberecord",
            name="plateau",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="probes",
                to="probes.plateaurecord",
            ),
        ),
        migrations.RunPython(
            forwards_link_probes_to_plateaus, migrations.RunPython.noop
        ),
        migrations.AlterField(
            model_name="proberecord",
            name="plateau",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="probes",
                to="probes.plateaurecord",
            ),
        ),
        migrations.RemoveField(
            model_name="proberecord",
            name="plateau_max_x",
        ),
        migrations.RemoveField(
            model_name="proberecord",
            name="plateau_max_y",
        ),
        migrations.AddConstraint(
            model_name="proberecord",
            constraint=models.UniqueConstraint(
                fields=("plateau", "x", "y"),
                name="unique_probe_position_per_plateau",
            ),
        ),
    ]
