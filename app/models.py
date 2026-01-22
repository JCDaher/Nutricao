"""
Pydantic models for the diabetes diet generator
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class PatientData(BaseModel):
    """Dados do paciente coletados do formulário"""
    nome: str = Field(..., min_length=3, description="Nome completo do paciente")
    sexo: str = Field(..., pattern="^(M|F)$", description="Sexo: M ou F")
    idade: int = Field(..., ge=18, le=100, description="Idade em anos")
    peso: float = Field(..., ge=40, le=300, description="Peso em kg")
    altura: float = Field(..., ge=140, le=220, description="Altura em cm")
    hba1c: Optional[float] = Field(None, ge=4, le=15, description="HbA1c em %")
    glicemia: Optional[float] = Field(None, ge=70, le=400, description="Glicemia em mg/dL")


class NutritionData(BaseModel):
    """Dados nutricionais calculados localmente"""
    tmb: float = Field(..., description="Taxa Metabólica Basal em kcal")
    necessidade_calorica: float = Field(..., description="Necessidade calórica total em kcal/dia")
    meta_calorica: float = Field(..., description="Meta calórica ajustada em kcal/dia")
    imc: float = Field(..., description="Índice de Massa Corporal")
    macros: Dict[str, float] = Field(..., description="Distribuição de macronutrientes")
    distribuicao_refeicoes: Dict[str, Dict] = Field(..., description="Distribuição de calorias por refeição")


class FoodItem(BaseModel):
    """Item alimentar individual"""
    nome: str = Field(..., description="Nome do alimento")
    porcao: str = Field(..., description="Porção em medida caseira")
    gramas: float = Field(..., description="Quantidade em gramas")
    kcal: float = Field(..., description="Calorias")
    carb: float = Field(..., description="Carboidratos em g")
    prot: float = Field(..., description="Proteínas em g")
    gord: float = Field(..., description="Gorduras em g")
    fibra: float = Field(0, description="Fibras em g")


class Meal(BaseModel):
    """Estrutura de uma refeição"""
    nome: str = Field(..., description="Nome da refeição")
    horario: str = Field(..., description="Horário sugerido")
    calorias_alvo: float = Field(..., description="Calorias alvo para a refeição")
    alimentos: List[FoodItem] = Field(default_factory=list, description="Lista de alimentos")

    @property
    def calorias_total(self) -> float:
        """Calcula o total de calorias da refeição"""
        return sum(a.kcal for a in self.alimentos)

    @property
    def carb_total(self) -> float:
        """Calcula o total de carboidratos da refeição"""
        return sum(a.carb for a in self.alimentos)

    @property
    def prot_total(self) -> float:
        """Calcula o total de proteínas da refeição"""
        return sum(a.prot for a in self.alimentos)

    @property
    def gord_total(self) -> float:
        """Calcula o total de gorduras da refeição"""
        return sum(a.gord for a in self.alimentos)


class DietPlan(BaseModel):
    """Plano alimentar completo estruturado"""
    paciente: PatientData
    calculos: NutritionData
    refeicoes: List[Meal]

    @property
    def calorias_total(self) -> float:
        """Calcula o total de calorias do plano"""
        return sum(r.calorias_total for r in self.refeicoes)
