using System;
using System.Collections;
using System.Collections.Generic;
using System.Reflection.Emit;
using UnityEditor;
using UnityEditorInternal;
using UnityEngine;

public class Player : MonoBehaviour
{
    PlayerInput playerInput ;
    [SerializeField] Transform[] LaneTransForm;
    [SerializeField] float JumpHeight = 1.0f;
    [SerializeField] Transform GrounCheckTransform;
    [SerializeField] [Range(0,1)] float GroundCheckRadius = 0.2f;
    [SerializeField] LayerMask GroundCheckMask;
    Vector3 Destination;
    int CurrentLane;
    private void OnEnable() 
    {
        if(playerInput==null){
            playerInput = new PlayerInput();
        }
        playerInput.Enable();
    }
    private void OnDisable() 
    {
        playerInput.Disable();   
    }
    // Start is called before the first frame update
    void Start()
    {
        for(int i=0;i<LaneTransForm.Length;i++){
            if(LaneTransForm[i].position == transform.position){
                CurrentLane = i;
                Destination = LaneTransForm[i].position;
            }
        };
        playerInput.gameplay.Move.performed += MovePerformed;
        playerInput.gameplay.Jump.performed += JumpPerformed;
    }



    private void MoveLeft(){
        if(CurrentLane == 0){
            return;
        };
        CurrentLane--;
        Destination = LaneTransForm[CurrentLane].position;
    }
    private void MoveRight(){
        if(CurrentLane == LaneTransForm.Length -1){
            return;
        };
        CurrentLane++;
        Destination = LaneTransForm[CurrentLane].position;

    }
    private void MovePerformed(UnityEngine.InputSystem.InputAction.CallbackContext context)
    {
        float InputValue = context.ReadValue<float>();
        if(InputValue >0){
            MoveRight();
        }else if(InputValue < 0){
            MoveLeft();
        }
        Debug.Log($"移动操作生效了，其值为{InputValue}");
    }
    private void JumpPerformed(UnityEngine.InputSystem.InputAction.CallbackContext context)
    {
        Rigidbody rigidbody = GetComponent<Rigidbody>();
        if(rigidbody!=null){
            float JumpSpeed = Mathf.Sqrt(2*JumpHeight*Physics.gravity.magnitude);
            rigidbody.AddForce(new Vector3(0,JumpSpeed,0),ForceMode.VelocityChange);
        };
    }
    // Update is called once per frame
    void Update()
    {
        float TransformX = Mathf.Lerp(transform.position.x,Destination.x,Time.deltaTime*5);     
        transform.position = new Vector3(TransformX,transform.position.y,transform.position.z);   
        if(!IsOnGround()){
            Debug.Log("不在地面上");
            OnDisable();
        }else{
            Debug.Log("在地面上");
            OnEnable();
        }
    }

    bool IsOnGround(){
        return Physics.CheckSphere(GrounCheckTransform.position,GroundCheckRadius,GroundCheckMask);
    }
}
