from app.generators.sysml_pipeline import generate_l1_sysml


output_path = "generated/sysml/L1_TwoTankController.sysml"

result = generate_l1_sysml(output_path)

print(f"Generated SysML: {result}")