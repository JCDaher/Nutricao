"""
Serviço de integração com API FEEGOW
Permite buscar pacientes e fazer upload de arquivos no prontuário
"""
import httpx
from typing import Optional, List, Dict, Any
from datetime import datetime
import base64

from app.config.settings import settings


class FeegowService:
    """
    Cliente para API FEEGOW
    Documentação: https://docs.feegow.com/
    """

    def __init__(self, token: str = None):
        self.token = token or settings.feegow_api_token
        self.base_url = settings.feegow_api_url
        self.headers = {
            "x-access-token": self.token,
            "Content-Type": "application/json"
        }

    @property
    def is_configured(self) -> bool:
        """Verifica se a API está configurada"""
        return bool(self.token)

    async def search_patients(
        self,
        nome: str = None,
        cpf: str = None,
        prontuario: str = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Busca pacientes no FEEGOW

        Args:
            nome: Nome do paciente (busca parcial)
            cpf: CPF do paciente
            prontuario: Número do prontuário
            limit: Limite de resultados

        Returns:
            Dict com lista de pacientes encontrados
        """
        if not self.is_configured:
            return {"success": False, "error": "FEEGOW não configurado"}

        try:
            params = {"limit": limit}

            if nome:
                params["nome"] = nome
            if cpf:
                params["cpf"] = cpf.replace(".", "").replace("-", "")
            if prontuario:
                params["local_id"] = prontuario

            async with httpx.AsyncClient(timeout=30.0) as client:
                # Tentar endpoint /patient/list primeiro
                response = await client.get(
                    f"{self.base_url}/patient/list",
                    headers=self.headers,
                    params=params
                )

                if response.status_code == 200:
                    data = response.json()
                    patients = data.get("content", data.get("data", []))

                    # Se for uma lista direta
                    if isinstance(patients, dict):
                        patients = [patients]

                    # Formatar dados dos pacientes
                    formatted_patients = []
                    for p in patients:
                        formatted_patients.append({
                            "id": p.get("patient_id") or p.get("id") or p.get("paciente_id"),
                            "prontuario": p.get("local_id") or p.get("prontuario"),
                            "nome": p.get("nome") or p.get("nomePaciente"),
                            "cpf": p.get("cpf") or p.get("cpfPaciente"),
                            "data_nascimento": p.get("nascimento") or p.get("data_nascimento"),
                            "sexo": self._parse_sexo(p.get("sexo") or p.get("sexo_id")),
                            "telefone": p.get("celular") or p.get("telefone") or p.get("cel1") or p.get("tel1"),
                            "email": p.get("email"),
                            "peso": self._parse_float(p.get("peso")),
                            "altura": self._parse_float(p.get("altura")),
                        })

                    # Filtrar localmente já que a API FEEGOW não suporta filtro
                    if nome:
                        nome_lower = nome.lower()
                        formatted_patients = [
                            p for p in formatted_patients
                            if p.get("nome") and nome_lower in p["nome"].lower()
                        ]
                    if cpf:
                        cpf_clean = cpf.replace(".", "").replace("-", "")
                        formatted_patients = [
                            p for p in formatted_patients
                            if p.get("cpf") and cpf_clean in p["cpf"].replace(".", "").replace("-", "")
                        ]
                    if prontuario:
                        formatted_patients = [
                            p for p in formatted_patients
                            if p.get("prontuario") and prontuario in str(p["prontuario"])
                        ]

                    # Limitar resultados
                    formatted_patients = formatted_patients[:limit]

                    return {
                        "success": True,
                        "patients": formatted_patients,
                        "total": len(formatted_patients)
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Erro na API: {response.status_code}",
                        "detail": response.text
                    }

        except httpx.TimeoutException:
            return {"success": False, "error": "Timeout na conexão com FEEGOW"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _parse_sexo(self, sexo) -> str:
        """Converte sexo para M ou F"""
        if not sexo:
            return ""
        sexo_str = str(sexo).lower()
        if sexo_str in ["m", "masculino", "male"]:
            return "M"
        elif sexo_str in ["f", "feminino", "female"]:
            return "F"
        return sexo_str.upper()[:1] if sexo_str else ""

    async def get_patient(self, patient_id: int) -> Dict[str, Any]:
        """
        Busca dados completos de um paciente pelo ID

        Args:
            patient_id: ID do paciente no FEEGOW

        Returns:
            Dict com dados completos do paciente
        """
        if not self.is_configured:
            return {"success": False, "error": "FEEGOW não configurado"}

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/patient/get",
                    headers=self.headers,
                    params={"id": patient_id}
                )

                if response.status_code == 200:
                    data = response.json()
                    p = data.get("content", {})

                    # Calcular idade a partir da data de nascimento
                    idade = None
                    if p.get("nascimento"):
                        try:
                            nasc = datetime.strptime(p["nascimento"], "%Y-%m-%d")
                            hoje = datetime.now()
                            idade = hoje.year - nasc.year - (
                                (hoje.month, hoje.day) < (nasc.month, nasc.day)
                            )
                        except:
                            pass

                    return {
                        "success": True,
                        "patient": {
                            "id": p.get("id"),
                            "prontuario": p.get("local_id") or p.get("prontuario"),
                            "nome": p.get("nome"),
                            "cpf": p.get("cpf"),
                            "data_nascimento": p.get("nascimento"),
                            "idade": idade,
                            "sexo": "M" if p.get("sexo") == "Masculino" else "F",
                            "telefone": p.get("celular") or p.get("telefone"),
                            "email": p.get("email"),
                            "peso": self._parse_float(p.get("peso")),
                            "altura": self._parse_float(p.get("altura")),
                            "endereco": {
                                "logradouro": p.get("logradouro"),
                                "numero": p.get("numero"),
                                "bairro": p.get("bairro"),
                                "cidade": p.get("cidade"),
                                "estado": p.get("estado"),
                                "cep": p.get("cep")
                            }
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Erro na API: {response.status_code}"
                    }

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def upload_diet_to_record(
        self,
        patient_id: int,
        diet_content: str,
        filename: str,
        description: str = "Plano Alimentar Personalizado"
    ) -> Dict[str, Any]:
        """
        Faz upload da dieta para o prontuário do paciente

        Args:
            patient_id: ID do paciente no FEEGOW
            diet_content: Conteúdo da dieta em Markdown
            filename: Nome do arquivo
            description: Descrição do arquivo

        Returns:
            Dict com resultado do upload
        """
        if not self.is_configured:
            return {"success": False, "error": "FEEGOW não configurado"}

        try:
            # Converter conteúdo para base64
            content_bytes = diet_content.encode('utf-8')
            content_base64 = base64.b64encode(content_bytes).decode('utf-8')

            payload = {
                "paciente_id": patient_id,
                "arquivo": content_base64,
                "nome_arquivo": filename,
                "descricao": description,
                "tipo": "text/markdown"
            }

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/patient/upload-file",
                    headers=self.headers,
                    json=payload
                )

                if response.status_code in [200, 201]:
                    return {
                        "success": True,
                        "message": "Dieta enviada para o prontuário com sucesso"
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Erro no upload: {response.status_code}",
                        "detail": response.text
                    }

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def list_patient_files(self, patient_id: int) -> Dict[str, Any]:
        """
        Lista arquivos do prontuário do paciente

        Args:
            patient_id: ID do paciente no FEEGOW

        Returns:
            Dict com lista de arquivos
        """
        if not self.is_configured:
            return {"success": False, "error": "FEEGOW não configurado"}

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/patient/files",
                    headers=self.headers,
                    params={"paciente_id": patient_id}
                )

                if response.status_code == 200:
                    data = response.json()
                    return {
                        "success": True,
                        "files": data.get("content", [])
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Erro na API: {response.status_code}"
                    }

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def create_patient(
        self,
        nome: str,
        sexo: str,
        data_nascimento: str = None,
        cpf: str = None,
        telefone: str = None,
        email: str = None,
        peso: float = None,
        altura: float = None
    ) -> Dict[str, Any]:
        """
        Cria um novo paciente no FEEGOW

        Args:
            nome: Nome completo do paciente (obrigatório)
            sexo: Sexo do paciente - M ou F (obrigatório)
            data_nascimento: Data de nascimento no formato YYYY-MM-DD
            cpf: CPF do paciente
            telefone: Telefone do paciente
            email: Email do paciente
            peso: Peso em kg
            altura: Altura em cm

        Returns:
            Dict com dados do paciente criado
        """
        if not self.is_configured:
            return {"success": False, "error": "FEEGOW não configurado"}

        if not nome or not sexo:
            return {"success": False, "error": "Nome e sexo são obrigatórios"}

        try:
            # Montar payload conforme API FEEGOW
            payload = {
                "nome": nome,
                "sexo": "Masculino" if sexo == "M" else "Feminino"
            }

            if data_nascimento:
                payload["nascimento"] = data_nascimento
            if cpf:
                # Remover formatação do CPF
                payload["cpf"] = cpf.replace(".", "").replace("-", "")
            if telefone:
                payload["celular"] = telefone
            if email:
                payload["email"] = email
            if peso:
                payload["peso"] = str(peso)
            if altura:
                # FEEGOW pode aceitar altura em metros ou cm
                payload["altura"] = str(altura)

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/patient/new",
                    headers=self.headers,
                    json=payload
                )

                if response.status_code in [200, 201]:
                    data = response.json()
                    content = data.get("content", {})

                    # Retornar dados do paciente criado
                    return {
                        "success": True,
                        "message": "Paciente criado com sucesso",
                        "patient": {
                            "id": content.get("id"),
                            "prontuario": content.get("local_id") or content.get("prontuario"),
                            "nome": nome,
                            "sexo": sexo,
                            "data_nascimento": data_nascimento,
                            "cpf": cpf,
                            "telefone": telefone,
                            "email": email,
                            "peso": peso,
                            "altura": altura
                        }
                    }
                elif response.status_code == 409:
                    return {
                        "success": False,
                        "error": "Paciente já existe no sistema (CPF duplicado)"
                    }
                else:
                    error_detail = response.text
                    try:
                        error_json = response.json()
                        error_detail = error_json.get("message", error_detail)
                    except:
                        pass
                    return {
                        "success": False,
                        "error": f"Erro ao criar paciente: {response.status_code}",
                        "detail": error_detail
                    }

        except httpx.TimeoutException:
            return {"success": False, "error": "Timeout na conexão com FEEGOW"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _parse_float(self, value) -> Optional[float]:
        """Converte valor para float de forma segura"""
        if value is None:
            return None
        try:
            return float(str(value).replace(",", "."))
        except:
            return None


# Instância global
feegow_service = FeegowService()
