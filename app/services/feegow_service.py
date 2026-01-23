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
                params["cpf"] = cpf
            if prontuario:
                params["prontuario"] = prontuario

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/patient/search",
                    headers=self.headers,
                    params=params
                )

                if response.status_code == 200:
                    data = response.json()
                    patients = data.get("content", [])

                    # Formatar dados dos pacientes
                    formatted_patients = []
                    for p in patients:
                        formatted_patients.append({
                            "id": p.get("id"),
                            "prontuario": p.get("local_id") or p.get("prontuario"),
                            "nome": p.get("nome"),
                            "cpf": p.get("cpf"),
                            "data_nascimento": p.get("nascimento"),
                            "sexo": "M" if p.get("sexo") == "Masculino" else "F",
                            "telefone": p.get("celular") or p.get("telefone"),
                            "email": p.get("email"),
                            "peso": p.get("peso"),
                            "altura": p.get("altura"),
                        })

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
