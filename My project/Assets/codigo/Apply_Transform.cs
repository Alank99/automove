/*
the matrices to modify the vertices of mesh using basic transforms
*/

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Apply_Transform : MonoBehaviour
{
    [SerializeField] Vector3 displacement;
    [SerializeField] float angle;
    [SerializeField] AXIS rotationAxis;
    
    [SerializeField] GameObject llanta;

    [SerializeField] float speed;

    //un arrego de las posiciones de las llantas
    [SerializeField] Vector3[] llantasPos;

    Mesh mesh; //serie de puntos mezcladas
    Mesh llantaMesh1, llantaMesh2, llantaMesh3, llantaMesh4;
    Vector3[] baseVertices;
    Vector3[] newVectices;

    Vector3[] llantasVertices1;
    Vector3[] llantasNewVertices1;

    Vector3[] llantasVertices2;
    Vector3[] llantasNewVertices2;

    Vector3[] llantasVertices3;
    Vector3[] llantasNewVertices3;

    Vector3[] llantasVertices4;
    Vector3[] llantasNewVertices4;



    // Start is called before the first frame update
    void Start()
    {
        
        mesh = GetComponentInChildren<MeshFilter>().mesh;
        baseVertices = mesh.vertices;
        
        newVectices = new Vector3[baseVertices.Length];
        for (int i = 0; i < baseVertices.Length; i++)
        {
            newVectices[i] = baseVertices[i];
        }
        generateLlantas();

    }



    // Update is called once per frame
    void Update()
    {
       angle = GetAngle(displacement);
       DoTransform();
       
    }

    float GetAngle(Vector3 displacement)
    {
        float a = Mathf.Atan2(displacement.x, displacement.z) ; //debe ser asi el auto como las llantas apunta en z siendo el angulo 0
        return a * Mathf.Rad2Deg;
    }

    void DoTransform()
    {
        Matrix4x4 move = HW_Transforms.TranslationMat(displacement.x * Time.time,
                                                    displacement.y * Time.time,
                                                    displacement.z * Time.time);

        Matrix4x4 rotate = HW_Transforms.RotateMat(angle , rotationAxis);

        Matrix4x4 composite =  move * rotate ;

        Matrix4x4 rotateLlantas = HW_Transforms.RotateMat(Time.time * speed , AXIS.X) ;
        Matrix4x4 posicionLlantas1 = HW_Transforms.TranslationMat(llantasPos[0].x,llantasPos[0].y ,llantasPos[0].z );
        Matrix4x4 posicionLlantas2 = HW_Transforms.TranslationMat(llantasPos[1].x,llantasPos[1].y ,llantasPos[1].z );
        Matrix4x4 posicionLlantas3 = HW_Transforms.TranslationMat(llantasPos[2].x,llantasPos[2].y ,llantasPos[2].z );
        Matrix4x4 posicionLlantas4 = HW_Transforms.TranslationMat(llantasPos[3].x,llantasPos[3].y ,llantasPos[3].z );

        Matrix4x4 compositeLlantas1 =  composite * posicionLlantas1 * rotateLlantas;
        Matrix4x4 compositetest =  posicionLlantas1 * rotateLlantas;

        Matrix4x4 compositeLlantas2 =  composite * posicionLlantas2 * rotateLlantas;
        Matrix4x4 compositeLlantas3 =  composite * posicionLlantas3 * rotateLlantas;
        Matrix4x4 compositeLlantas4 =  composite * posicionLlantas4 * rotateLlantas;
    

        for (int i = 0; i < newVectices.Length; i++)
        {
            Vector4 temp= new Vector4(baseVertices[i].x, baseVertices[i].y, baseVertices[i].z, 1);
            
            newVectices[i] = composite * temp;
        }



        for (int i = 0; i < llantasNewVertices1.Length; i++)
        {
            Vector4 temp1= new Vector4(llantasVertices1[i].x, llantasVertices1[i].y, llantasVertices1[i].z, 1);

            llantasNewVertices1[i] = compositetest * temp1;
            llantasNewVertices2[i] = compositeLlantas2 * temp1;
            llantasNewVertices3[i] = compositeLlantas3 * temp1;
            llantasNewVertices4[i] = compositeLlantas4 * temp1;

            
        }

        mesh.vertices = newVectices;
        mesh.RecalculateNormals();

        llantaMesh1.vertices = llantasNewVertices1;
        llantaMesh1.RecalculateNormals();
        llantaMesh2.vertices = llantasNewVertices2;
        llantaMesh2.RecalculateNormals();
        llantaMesh3.vertices = llantasNewVertices3;
        llantaMesh3.RecalculateNormals();
        llantaMesh4.vertices = llantasNewVertices4;
        llantaMesh4.RecalculateNormals();
                                                    
    }  

    void generateLlantas()
    {
        Vector3 posicion_original = new Vector3(0,0,0) ;
        for (int i = 0; i < llantasPos.Length; i++)
        {
            GameObject llantaTemp = Instantiate(llanta, posicion_original  , Quaternion.identity);
            switch(i){
                case 0:
                    llantaMesh1 = llantaTemp.GetComponentInChildren<MeshFilter>().mesh;
                    llantasVertices1 = llantaMesh1.vertices;
                    llantasNewVertices1 = new Vector3[llantasVertices1.Length];
                    for (int j = 0; j < llantasVertices1.Length; j++)
                    {
                        llantasNewVertices1[j] = llantasVertices1[j];
                    }
                    break;
                case 1:
                    llantaMesh2 = llantaTemp.GetComponentInChildren<MeshFilter>().mesh;
                    llantasVertices2 = llantaMesh2.vertices;
                    llantasNewVertices2 = new Vector3[llantasVertices2.Length];
                    for (int j = 0; j < llantasVertices2.Length; j++)
                    {
                        llantasNewVertices2[j] = llantasVertices2[j];
                    }
                    break;
                case 2:
                    llantaMesh3 = llantaTemp.GetComponentInChildren<MeshFilter>().mesh;
                    llantasVertices3 = llantaMesh3.vertices;
                    llantasNewVertices3 = new Vector3[llantasVertices3.Length];
                    for (int j = 0; j < llantasVertices3.Length; j++)
                    {
                        llantasNewVertices3[j] = llantasVertices3[j];
                    }
                    break;
                case 3:
                    llantaMesh4 = llantaTemp.GetComponentInChildren<MeshFilter>().mesh;
                    llantasVertices4 = llantaMesh4.vertices;
                    llantasNewVertices4 = new Vector3[llantasVertices4.Length];
                    for (int j = 0; j < llantasVertices4.Length; j++)
                    {
                        llantasNewVertices4[j] = llantasVertices4[j];
                    }
                    break;
            }
        }
    }

}
